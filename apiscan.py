#!/usr/bin/python3
# Author: Scragg
# Date: 22/03/2023
# -------------------
# APIScan is a tool that helps keep track of API endpoints and responses for each accepted method.
# -------------------

# Imports
import os, sys, time, requests, json
from art import *

# Variables
outfile = ''
outfile_name = 'res.txt'
endpoints = []
cmd = ''
target = ''
custom_headers = {}
aggressive_mode = False
delete_mode = False

# Decorators
def timer(func):
	def wrapper(arg):
		start = time.time()
		ret = func(arg)
		exec_time = time.time()-start
		print('Executed in', exec_time, 'seconds.')
		return ret
	return wrapper

def main():
	global cmd, endpoints, outfile, target, custom_headers, aggressive_mode, delete_mode
	print(text2art('APIScan'),'\r\t\t    By Scragg\n'+'-'*48)
	while(cmd != 'exit'):
		cmd = input('\u001b[36mapiscan\u001b[33m>\u001b[37m ')
		if cmd == 'help':
			print('-- APIScan --\n\tstart - Start scan loop, enter endpoints one by one.'
				+'\n\t\\save - Save and terminate current scan.'
				+'\n\t\\setheader - Set a custom header to send in requests.'
				+'\n\t\\removeheader - Remove a custom header by name.'
				+'\n\t\\listheaders - List all custom headers and values.'
				+'\n\t\\aggressive - Attempt all methods, except DELETE.'
				+'\n\t\\delete - Attempt DELETE method.'
				+'\n\t\\standard - Attempt all methods returned by OPTIONS request.'
				+'\n\texit - Exit APIScan.'
				+'\n\thelp or \\help - Dispaly this message.')
		elif cmd == 'start':
			outfile = open(outfile_name, 'a')
			print('\u001b[36mType \'exit\' to save results and end the scan.\u001b[37m')
			target = input('\u001b[32mTarget \u001b[33mhttp(s)://ip:port\u001b[32m>\u001b[37m')
			ep = input('\u001b[32mendpoint\u001b[31m>\u001b[37m ')
			while(ep != '\\save'):
				if ep == '':
					ep = '/'
				elif ep == '\\setheader':
					name = input("\u001b[33mHeader name\u001b[31m>\u001b[37m ")
					value = input("\u001b[33mHeader value\u001b[31m>\u001b[37m ")
					custom_headers[name] = value
					ep = input('\u001b[32mendpoint\u001b[31m>\u001b[37m ')
					continue
				elif ep == '\\removeheader':
					name = input("\u001b[33mHeader name\u001b[31m>\u001b[37m ")
					del custom_headers[name]
					ep = input('\u001b[32mendpoint\u001b[31m>\u001b[37m ')
					continue
				elif ep == '\\listheaders':
					for h in custom_headers:
						print('\t'+h+': '+custom_headers[h])
					ep = input('\u001b[32mendpoint\u001b[31m>\u001b[37m ')
					continue
				elif ep == '\\aggressive':
					aggressive_mode = True
					delete_mode = False
					ep = input('\u001b[32mendpoint\u001b[31m>\u001b[37m ')
					continue
				elif ep == '\\delete':
					aggressive_mode = False
					delete_mode = True
					ep = input('\u001b[32mendpoint\u001b[31m>\u001b[37m ')
					continue
				elif ep == '\\standard':
					delete_mode = False
					aggressive_mode = False
					ep = input('\u001b[32mendpoint\u001b[31m>\u001b[37m ')
					continue
				elif ep == '\\help':
					print('-- APIScan --\n\tstart - Start scan loop, enter endpoints one by one.'
						+'\n\t\\save - Save and terminate current scan.'
						+'\n\t\\setheader - Set a custom header to send in requests.'
						+'\n\t\\removeheader - Remove a custom header by name.'
						+'\n\t\\listheaders - List all custom headers and values.'
						+'\n\t\\aggressive - Attempt all methods, except DELETE.'
						+'\n\t\\delete - Attempt DELETE method.'
						+'\n\t\\standard - Attempt all methods returned by OPTIONS request.'
						+'\n\texit - Exit APIScan.'
						+'\n\thelp or \\help - Dispaly this message.')
					ep = input('\u001b[32mendpoint\u001b[31m>\u001b[37m ')
					continue
				elif ep[0] != '/':
					ep = '/'+ep
				res = checkEndpoint(ep)
				outfile.write(str('\n'+'-'*25+'\n'+str(res)))
				ep = input('\u001b[32mendpoint\u001b[31m>\u001b[37m ')
			outfile.write(str('\n'+'-'*25))
			outfile.close()
	return

@timer
def checkEndpoint(ep):
	global custom_headers, aggressive_mode, delete_mode
	out = ''
	endpoint = target+ep
	methods = requests.request('OPTIONS', endpoint, headers=custom_headers).headers['Allow']
	out = 'Endpoint:\t'+endpoint+'\nMethods:\t'+methods
	loop_methods = methods.split(', ')
	if aggressive_mode:
		loop_methods = ['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'TRACE', 'CONNECT']
	if delete_mode:
		loop_methods = ['DELETE']
	for i in loop_methods:
		# Loop through methods and get responses
		res = requests.request(i, endpoint, headers=custom_headers)
		headers = ''
		for h,v in res.headers.items():
			headers = headers+'\n\t\t'+h+":\t"+v
		body = ''
		try:
			data = json.loads(res.text)
			body = ' JSON'
			for d in data:
				body = body+"\n\t\t"+d+":\t"+data[d]
		except:
			for b in res.text.split('\n'):
				body = body+"\n\t\t"+b
		out = out+str("\n"+i+": "+str(res.status_code)+"\n\tHeaders:"+str(headers)+"\n\tBody:"+body+"\n")
	print(out)
	return str(out)

if __name__ == '__main__':
	main()
