#!/usr/bin/env bash
echo $(date) >> /home/vagrant/generate_crt.log
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
#удаляем просроченные сертификаты:
if vault write pki_int/tidy tidy_cert_store=true tidy_revoked_certs=true
then
	echo "Expired cert removed" >> /home/vagrant/generate_crt.log
fi

#Запрашиваем новый сертификат
if vault write -format=json pki_int/issue/example-dot-com common_name="example.com" ttl="720h" > /home/vagrant/example.com.crt
then
	echo "New cert issued" >> /home/vagrant/generate_crt.log
	#Разбираем его на 2 файла - pem и key
	cat /home/vagrant/example.com.crt | jq -r .data.certificate > /home/vagrant/example.com.crt.pem
	cat /home/vagrant/example.com.crt | jq -r .data.ca_chain[] >> /home/vagrant/example.com.crt.pem
	cat /home/vagrant/example.com.crt | jq -r .data.private_key > /home/vagrant/example.com.crt.key
	expire=`cat /home/vagrant/example.com.crt | jq -r .data.expiration`
	echo "Expiration date: " `date -d @$expire` >> /home/vagrant/generate_crt.log
	#Проверяем конфигурацию nginx	
	if nginx -t
	then
		echo "Nginx config test passed" >> /home/vagrant/generate_crt.log
		#Перезагружаем nginx
		if systemctl reload nginx
		then
			echo "Nginx succsessfully reloaded" >> /home/vagrant/generate_crt.log
		else
			echo "Error reload Nginx" >> /home/vagrant/generate_crt.log
		fi
	else
		echo "Error config Nginx" >> /home/vagrant/generate_crt.log
	fi
else
	echo "Error. New cert not issued" >> /home/vagrant/generate_crt.log
fi

