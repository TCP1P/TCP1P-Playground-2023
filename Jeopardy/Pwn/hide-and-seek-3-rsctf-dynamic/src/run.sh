#!/bin/bash

socat tcp-l:10000,reuseaddr,fork exec:./chall,stderr
