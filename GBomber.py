#!/usr/bin/python3

import signal
import smtplib
import getpass
from pwn import *

#Colors
class colors:
	RED = "\033[1;31m\033[1m"
	YELLOW = "\033[0;33m\033[1m"
	GREEN = "\033[0;32m\033[1m"
	BLUE = "\033[0;36m\033[1m"
	PURPLE = "\033[0;35m\033[1m"
	GRAY = "\033[0;37m\033[1m"
	END = "\033[0m"

def banner():
	print(colors.BLUE + "\n   ___     ___                    _\n  / __|   | _ )    ___    _ __   | |__     ___      _ _  \t\t\t\t" + colors.GRAY + "BY" + colors.YELLOW + " Invertebrado")
	print(colors.BLUE + " | (_ |   | _ \   / _ \  | '  \  | '_ \   / -_)    | '_|")
	print(colors.BLUE + "  \___|   |___/   \___/  |_|_|_| |_.__/   \___|   _|_|_\t" + colors.GRAY + "PERSONAL PAGE" + colors.GREEN + " https://invertebr4do.github.io")
	print(colors.BLUE + "_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|  \t" + colors.GRAY + "GITHUB" + colors.PURPLE + " https://github.com/Invertebr4do")
	print(colors.BLUE + " `-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'" + colors.END)

def def_handler(sig, frame):
	print(colors.RED + "\n[!] Exiting..." + colors.END)

	if threading.activeCount() > 1:
		os.system("tput cnorm")
		os._exit(getattr(os, "_exitcode", 0))
	else:
		os.system("tput cnorm")
		sys.exit(getattr(os, "_exitcode", 0))

signal.signal(signal.SIGINT, def_handler)

subject = open("subject_content.txt", "r")
content = open("message_content.txt", "r")

banner()

from_address = input(str("\n" + colors.GREEN + "█" + colors.GRAY + " Enter your attacker email" + colors.GREEN + " >> " + colors.END))
to_address = input(str(colors.GREEN + "█" + colors.GRAY + " Enter the victim email" + colors.GREEN + " >> " + colors.END))

if '@' not in from_address or '@' not in to_address:
        print(colors.RED + "\n[-] Invalid email address" + colors.END)
        sys.exit(1)

elif 'gmail.' in from_address:
        WEmail = "smtp.gmail.com"

elif 'hotmail.' in from_address or 'outlook.' in from_address:
        WEmail = "smtp-mail.outlook.com"

elif 'yahoo.' in from_address:
        WEmail = "smtp.mail.yahoo.com"

else:
        print(colors.RED + "\n[-] Invalid email address" + colors.END)
        sys.exit(1)

m_t = input("\n" + colors.GREEN + "█" + colors.GRAY + " How many threads do you want to use? " + colors.PURPLE + "[less is better]" + colors.GREEN + " >> " + colors.END)

password = getpass.getpass(colors.PURPLE + "\n█" + colors.GRAY + " Enter the password for [%s] >> " % from_address.rstrip("\n"))

if len(password.rstrip()) < 1:
	print(colors.RED + "\n[-] Invalid password" + colors.END)
	sys.exit(1)

if int(m_t) < 1:
	m_t = 1

print("\n" + colors.PURPLE + "-"*80 + "\n" + colors.END)

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

			try:
				server = smtplib.SMTP(WEmail, 587)
				server.starttls()
				server.login(from_address, password)
				server.sendmail(from_address, to_address, message.encode('utf-8'))
				server.quit()

				p1.status("%d" % emails)
				emails += 1
				break

			except smtplib.SMTPAuthenticationError:
				print("\n" + colors.RED + "-"*80 + "\n█ Email or Password incorrect\n\n" + colors.YELLOW + "█ " + colors.GRAY +  "If your credentials are correct, enable less secure apps permisions " + colors.YELLOW + "█\n\n" + colors.RED + "█" + colors.GRAY + " Gmail" + colors.YELLOW + " >> " + colors.GRAY + "https://myaccount.google.com/lesssecureapps\n" + colors.PURPLE + "█" + colors.GRAY + " Yahoo" + colors.YELLOW + " >> " + colors.GRAY + "https://login.yahoo.com/account/security" + colors.END)
				if threading.activeCount() > 1:
					os.system("tput cnorm")
					os._exit(getattr(os, "_exitcode", 0))
				else:
					os.system("tput cnorm")
					sys.exit(getattr(os, "_exitcode", 0))

			except:
				log.failure("Failed to send, try again")
				if threading.activeCount() > 1:
					os.system("tput cnorm")
					os._exit(getattr(os, "_exitcode", 0))
				else:
					os.system("tput cnorm")
					sys.exit(getattr(os, "_exitcode", 0))

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
