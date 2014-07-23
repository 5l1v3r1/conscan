#!/usr/bin/python

## conscan.py
## Blackbox vulnerability scanne for the concrete5 CMS
## Detects concrete5 CMS, version and associated vulnerabilities
## Detects full path disclosure vulnerabilities
## Enumerates CMS users
## Brute-fores user account credentials

## import modules
try:
	import argparse
	import sys
	from modules import concrete
	from modules import login
	from modules import client

## Any import errors print to screen and exit
except Exception, error:
	print error
	sys.exit(1)


## Module used to print the banner
def banner():

   print """
   //========================================================================\\\\
   ||                                                                        ||
   || TITLE                                                                  ||
   || conscan.py                                                             ||
   ||                                                                        ||
   || DESCRIPTION                                                            ||
   || concrete5 blackbox vulnerability scanner              	             ||
   ||                                                                        ||
   || VERSION                                                                ||
   || 1.1                                                                    ||
   ||                                                                        ||
   || AUTHOR                                                                 ||
   || TheXero | thexero@nullsecurity.net                                     ||
   ||                                                                        ||
   || WEBSITE                                                                ||
   || www.thexero.co.uk | www.nullsecurity.net                               ||
   ||                                                                        ||
   \\\\========================================================================//
   """


## Module to sort out the program arguments
def arg_parser():

	parser = argparse.ArgumentParser(add_help=True,
	epilog='Example: ./%(prog)s -t https://www.thexero.co.uk:8443/concrete/ -e')

	parser.add_argument('-t', dest='target', help='Target IP / Domain', required='yes')
	parser.add_argument('-e', action='store_true', help='Perform enumeration')
	parser.add_argument('-u', dest='username', help='Username to login with')
	parser.add_argument('-p', dest='wordlist', help='Path to wordlist')
	parser.add_argument('--threads', dest='threads', help='Number of threads to be used for acount brute-force')

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	args = parser.parse_args()
	target = args.target

	if target.startswith("https://"):
		ssl = True
		target = target[8:]

	elif target.startswith("http://"):
		ssl = False
		target = target[7:]

	else:
		ssl = False

	if "/" in target:
		temp = target.split("/")
		target = temp[0]

		temp = temp[1:]

		dir = ''
		for item in temp:
			dir = dir + item + '/' 
	else:
		dir = '/'	

	if args.e:
        	enumerate = True
	else:
        	enumerate = False
	
	bruteforce = False	
	threads = 1
	wordlist = ''
	username = ''

	if args.username:
		if args.wordlist:
			username = args.username
			wordlist = args.wordlist
			bruteforce = True

			if args.threads:
				threads = int(args.threads)

		else:
			print "Path to wordlist needed to perform a bruteforce\n"
	                parser.print_help()
			sys.exit(1)		

	return target, dir, ssl, enumerate, bruteforce, username, wordlist, threads


## Program startup
if __name__ == '__main__':

	banner()
	target, dir, ssl, enumerate, bruteforce, username, wordlist, threads = arg_parser()

	concrete.detect(target, dir, ssl)

	if enumerate == True:
		concrete.enumerate(target, dir, ssl)

	if bruteforce == True:
               login.brute(target, dir, ssl, username, wordlist)		


	sys.exit(0)

