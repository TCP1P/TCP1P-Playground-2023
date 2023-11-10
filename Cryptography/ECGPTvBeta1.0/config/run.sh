#!/bin/sh
socat tcp-l:8010,reuseaddr,fork exec:"python3 chall.py"
