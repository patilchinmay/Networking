#!/usr/bin/env python

import paramiko
import time
import re
import sys

#Open SSHv2 connection to devices
def open_ssh_conn(ip):
    #Change exception message
    try:

        #Defining the commands file
        cmd_file = open('commands.txt','r')

        username = "teopy"
        
        password = "python"
        
        print "unsername "+username+" Password "+password

        #Logging into device
        session = paramiko.SSHClient()

        #paramiko.util.log_to_file("filename.log")
        
        #For testing purposes, this allows auto-accepting unknown host keys
        #Do not use in production! The default would be RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        #Passing the necessary parameters
        session.connect(hostname=ip, username="teopy", password="python")
        
        #Start an interactive shell session on the router
        connection = session.invoke_shell() 
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        time.sleep(1)
        
        #Entering global config mode
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)
        
        #Open user selected file for reading
        selected_cmd_file = open('commands.txt','r')
            
        #Starting from the beginning of the file
        selected_cmd_file.seek(0)
        
        #Writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)
        
        #Closing the command file
        selected_cmd_file.close()
        
        #Checking command output for IOS syntax errors
        output = connection.recv(65535)
        
        if re.search(r"% Invalid input detected at", output):
            print "* There was at least one IOS syntax error on device %s" % ip
        else:
            print "\nDONE for device %s" % ip
            
        #Test for reading command output
        print output + "\n"
        
        #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        print "* Invalid username or password. \n* Please check the username/password file or the device configuration!"
        print "* Closing program...\n"
        
#Calling the SSH function
ip = "192.168.2.101"
open_ssh_conn(ip)

# Important Resources
# On a linux machine:
# https://stackoverflow.com/questions/20840012/ssh-remote-host-identification-has-changed
# 'ssh username@host'

# On Router:
# '#sh ip ssh'
# '#ip ssh version 2'
# '#crypto key generate rsa' > 1024