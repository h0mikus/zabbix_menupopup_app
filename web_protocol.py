#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import configparser
import subprocess

config = configparser.ConfigParser()
config.read(os.path.split(sys.argv[0])[0] + '\\web_protocol.conf')

print(sys.argv)

def split_url(url):
	prepare_url = url.split(':') 

	while True:
		if (prepare_url[1][0:1] == '/'):
			prepare_url[1] = prepare_url[1][1:]
		else:
			break

	if (prepare_url[1][-1:] == '/'):
		prepare_url[1] = prepare_url[1][0:-1]


	if (len(prepare_url)<3):
		prepare_url.append('')

	if (prepare_url[2][-1:] == '/'):
		prepare_url[2] = prepare_url[2][0:-1]

	return prepare_url


if (len(sys.argv) > 1):
	protocol, ip, port = split_url(sys.argv[1])
	if (protocol in config.sections()):
		if (port == ''):
			#print(config[protocol]['path'] + ' ' + ip)
			subprocess.Popen(config[protocol]['path'] + ' ' + ip)
		elif (port != ''):
			#print(config[protocol]['path'] + ' ' + ip + config[protocol]['port_settings'][1:-1] + port)
			subprocess.Popen(config[protocol]['path'] + ' ' + ip + config[protocol]['port_settings'][1:-1] + port)
	else:
		input('Can not connect via "' + protocol + '"\nProtocol is not registred')

#print(protocol, ip, port)
#input()