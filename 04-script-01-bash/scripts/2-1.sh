#!/usr/bin/env bash
timeout=1
port=80
declare -i code
packet=5
array_ip=("192.168.0.1" "173.194.222.113" "87.250.250.242")
while ((1 == 1))
do
	for ip in ${array_ip[@]}
	do
		echo $ip >> curl.log
		p=0
		while (($p < $packet))
		do
			code=$(curl --write-out '%{http_code}' --silent --output /dev/null --connect-timeout $timeout http://$ip:$port)
			if (($code == 0))
			then
				echo $(date) "not responding" >> curl.log
			else
				echo $(date) "Code: " $code >> curl.log
			fi
        		p=$(($p+1))
		done
	done
done
