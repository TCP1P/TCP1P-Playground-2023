#!/bin/bash

socat tcp-l:9999,reuseaddr,fork exec:./chall,stderr
