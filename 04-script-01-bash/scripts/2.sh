#!/usr/bin/env bash
while ((1==1))
do
	curl https://localhost:9100
	if (($?!=0))
	then
		date >> curl.log
	else 
		break
	fi
done
