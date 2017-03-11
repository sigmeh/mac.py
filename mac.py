#!/usr/bin/env python
import subprocess as sp
import re
import sys
''' 
	Generate network interface dictionary data structure from ifconfig 
	utility and return available network interface MAC addresses.
	Argument 'all' passed during invocation prints all data on all interfaces.
'''

def main():
	args = sys.argv
	ifconfig = sp.Popen(['ifconfig'],stdout=sp.PIPE).communicate()[0]
	entries_split = re.findall('\n[^\t]',ifconfig)
	entries = []
	pos = 0
	for i in entries_split:
		split_pos = ifconfig.find(i,pos)
		if split_pos != -1:
			new_entry = ifconfig[pos:split_pos]
			pos += len(new_entry)+1
			entries.append( new_entry.strip() )
		else:
			entries.append( ifconfig[pos:] )
		
	interfaces = {}
	for i in entries:
		lines = [x.strip() for x in i.replace('\t','').split('\n') if x]
		lines_0_split = lines[0].split(':')
		interface  = lines_0_split[0]
		lines[0] = ''.join(lines_0_split[1:])
		ifdat = {}
		for line in lines:
			if '=' in line:
				line = line.split('=')
				key,val = line[0].strip(),''.join(line[1:])	
			else:
				split = line.find(' ')
				key,val = line[:split].strip().strip(':'),line[split:].strip()
			
			if not key in ifdat.keys():
				ifdat[key] = val
			else:
				if type(ifdat[key]) is str:
					ifdat[key] = [ ifdat[key],val ]
				elif type(ifdat[key]) is list:
					ifdat[key].append(val)
		interfaces[interface] = ifdat

	
	for i in sorted(interfaces.keys()):
		if sys.argv[-1] == 'all':
			print i
			for j in interfaces[i].keys():
				print ' ',j,' '*(11-len(j)),interfaces[i][j]
		else:
			if 'ether' in interfaces[i].keys() and 'status' in interfaces[i].keys():
				print i+':'+' '*(8-len(i))+interfaces[i]['ether']
				print ' '*9,interfaces[i]['status']

if __name__ == '__main__':
	main()