#!/bin/bash

##this should check ps and either start the server or leave it alone

##this should either return empty or will have a process ID
result=$(ps aux|grep "namebot5.3"|grep -v grep)
echo "we checked the ps and found it to be "  >> something.log
echo "'" >> something.log
echo $result >> something.log
echo "'" >> something.log

##react based on this
if [ -z  "$result" ];
then
	echo "nothing set this is not running" >>something.log;
	echo "starting a new instance" >> something.log
	/usr/bin/python3 /home/`whoami`/namebotmain/namebot5.3.py
	echo "tried to started bot" >> something.log
	newresult=$(ps aux|grep "namebot"|grep -v grep)
	if [ -z  "$result" ];
	then
		echo " it failed" >>something.log;
	else
		echo "it worked" >> something.log;
	fi;
else
	echo "we found something nothing to see here" >> something.log;
fi

