#!/usr/bin/env python

import subprocess as sp
from time import sleep

# set the path and filename for the file to hold your status information below:
filename = "~/someplace/.hiddenfolder/status.txt"

# set your mariadb username below:
username = "name_of_this_here_user"

main(filename, username)

def main(filename, username):
	is_active = check_status(filename)
	toggle(is_active, filename)
	login(username)

def start_db(filename):
	cmd = "sudo systemctl enable mariadb"
	sp.call(cmd, shell=True)
	
	# used to make sure the previous command has completed before the script attempts to perform subsequent steps
	cmd = 'sudo systemctl status mariadb | grep "Loaded: loaded" >>' + filename

	status_file = open(filename, "r")
	lines = status_file.readlines()

	while lines == "":
		print("Waiting on mariadb.service to load...")
		lines = getlines(status_file)

	status_file.close()
	
	erase_file(filename)
	
	cmd = "sudo systemctl start mariadb"
	sp.call(cmd, shell=True)
	
	return True

def login(username):
	cmd = "mariadb -u " + username + " -p"
	sp.call(cmd, shell=True)


def stop_db():
	cmd = "sudo systemctl stop mariadb"
	sp.call(cmd, shell=True)
	
	cmd = "sudo systemctl disable mariadb"
	sp.call(cmd, shell=True)
	
	return False


def toggle(is_active, filename):
	if is_active:
		stop_db()
	else:
		start_db(filename)
	

def check_status(filename):
	cmd = "sudo systemctl status mariadb >> " + filename
	
	sp.call(cmd, shell=True)

	status_file = open(filename, "r")
	results = status_file.readlines()
	status_file.close()
	erase_file(filename)
	for line in results:
		if "active (running)" in line:
			return True

	return False


def erase_file(filename):
	target_file = open(filename, "w")
	target_file.close()
