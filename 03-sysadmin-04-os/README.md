# Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

#### 1. На лекции мы познакомились с [node_exporter](https://github.com/prometheus/node_exporter/releases). В демонстрации его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. Используя знания из лекции по systemd, создайте самостоятельно простой [unit-файл](https://www.freedesktop.org/software/systemd/man/systemd.service.html) для node_exporter:

    * поместите его в автозагрузку,
    * предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на `systemctl cat cron`),
    * удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.

Для начала установим `node_exporter`:

```bash
01:58:58 with vagrant in ~ at vagrant took 6m 5s
➜ wget https://github.com/prometheus/node_exporter/releases/download/v\*/node_exporter-\*.\*-amd64.tar.gz
Warning: wildcards not supported in HTTP.
--2022-01-23 21:21:08--  https://github.com/prometheus/node_exporter/releases/download/v*/node_exporter-*.*-amd64.tar.gz
Resolving github.com (github.com)... 140.82.121.3
Connecting to github.com (github.com)|140.82.121.3|:443... connected.
HTTP request sent, awaiting response... 404 Not Found
2022-01-23 21:21:08 ERROR 404: Not Found.
```

При использовании `wget` из руководства [node_exporter](https://prometheus.io/docs/guides/node-exporter/) возникает ошибка, скачаем напрямую последний релиз:

```bash
21:29:35 with vagrant in ~ at vagrant
➜ wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
--2022-01-23 21:29:46--  https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
Resolving github.com (github.com)... 140.82.121.3
Connecting to github.com (github.com)|140.82.121.3|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://objects.githubusercontent.com/github-production-release-asset-2e65be/9524057/7c60f6f9-7b41-446c-be81-a6c24a9d0383?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20220123%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220123T212947Z&X-Amz-Expires=300&X-Amz-Signature=6bcb184970f5c092b984ee6d307bdbe02d64defd530c05351c10082b5ee29132&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=9524057&response-content-disposition=attachment%3B%20filename%3Dnode_exporter-1.3.1.linux-amd64.tar.gz&response-content-type=application%2Foctet-stream [following]
--2022-01-23 21:29:46--  https://objects.githubusercontent.com/github-production-release-asset-2e65be/9524057/7c60f6f9-7b41-446c-be81-a6c24a9d0383?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20220123%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220123T212947Z&X-Amz-Expires=300&X-Amz-Signature=6bcb184970f5c092b984ee6d307bdbe02d64defd530c05351c10082b5ee29132&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=9524057&response-content-disposition=attachment%3B%20filename%3Dnode_exporter-1.3.1.linux-amd64.tar.gz&response-content-type=application%2Foctet-stream
Resolving objects.githubusercontent.com (objects.githubusercontent.com)... 185.199.111.133, 185.199.110.133, 185.199.109.133, ...
Connecting to objects.githubusercontent.com (objects.githubusercontent.com)|185.199.111.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 9033415 (8.6M) [application/octet-stream]
Saving to: ‘node_exporter-1.3.1.linux-amd64.tar.gz’

node_exporter-1.3.1.linux-amd64.tar.gz        100%[================================================================================================>]   8.61M  9.62MB/s    in 0.9s

2022-01-23 21:29:48 (9.62 MB/s) - ‘node_exporter-1.3.1.linux-amd64.tar.gz’ saved [9033415/9033415]
```

Распакуем и перейдем в директорию установки:

```bash
21:30:44 with vagrant in ~ at vagrant
➜ tar xvfz node_exporter-1.3.1.linux-amd64.tar.gz
node_exporter-1.3.1.linux-amd64/
node_exporter-1.3.1.linux-amd64/LICENSE
node_exporter-1.3.1.linux-amd64/NOTICE
node_exporter-1.3.1.linux-amd64/node_exporter

21:30:56 with vagrant in ~ at vagrant
➜ cd node_exporter-1.3.1.linux-amd64
```

Скопируем исполняемый файл в `/usr/local/bin/`:
```bash
21:35:29 with vagrant in ~/node_exporter-1.3.1.linux-amd64 at vagrant
➜ sudo cp node_exporter /usr/local/bin/
```

Создадим пользователя `nodeusr` :

```bash
21:37:11 with vagrant in ~/node_exporter-1.3.1.linux-amd64 at vagrant
➜ sudo useradd --no-create-home --shell /bin/false nodeusr
```

Сделаем его владельцем исполняемого файла:

```bash
21:37:18 with vagrant in ~/node_exporter-1.3.1.linux-amd64 at vagrant
➜ sudo chown -R nodeusr:nodeusr /usr/local/bin/node_exporter
```

Создаем unit-файл `node_exporter.service` в `systemd`:

```bash
21:38:23 with vagrant in ~/node_exporter-1.3.1.linux-amd64 at vagrant
➜ sudo nano /etc/systemd/system/node_exporter.service
```

Следующего содержания:

```bash
[Unit]
Description=Node Exporter Service
After=network.target

[Service]
User=nodeusr
Group=nodeusr
Type=simple
ExecStart=/usr/local/bin/node_exporter $EXTRA_OPTS
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Перечитаем конфигурацию `systemd`:

```bash
21:47:14 with vagrant in ~/node_exporter-1.3.1.linux-amd64 at vagrant took 2m 56s
➜ sudo systemctl daemon-reload
```
Разрешим автозапуск:

```bash
21:47:48 with vagrant in ~/node_exporter-1.3.1.linux-amd64 at vagrant
➜ sudo systemctl enable node_exporter
Created symlink /etc/systemd/system/multi-user.target.wants/node_exporter.service → /etc/systemd/system/node_exporter.service.

```

Запускаем службу:

```bash
21:49:03 with vagrant in ~/node_exporter-1.3.1.linux-amd64 at vagrant
➜ sudo systemctl start node_exporter
```

Проверим статус службы:

```bash
21:49:49 with vagrant in ~/node_exporter-1.3.1.linux-amd64 at vagrant
➜ sudo systemctl status node_exporter
● node_exporter.service - Node Exporter Service
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2022-01-23 21:49:49 UTC; 19s ago
   Main PID: 8681 (node_exporter)
      Tasks: 4 (limit: 4617)
     Memory: 2.4M
     CGroup: /system.slice/node_exporter.service
             └─8681 /usr/local/bin/node_exporter

Jan 23 21:49:49 vagrant node_exporter[8681]: ts=2022-01-23T21:49:49.082Z caller=node_exporter.go:115 level=info collector=thermal_zone
Jan 23 21:49:49 vagrant node_exporter[8681]: ts=2022-01-23T21:49:49.082Z caller=node_exporter.go:115 level=info collector=time
Jan 23 21:49:49 vagrant node_exporter[8681]: ts=2022-01-23T21:49:49.084Z caller=node_exporter.go:115 level=info collector=timex
Jan 23 21:49:49 vagrant node_exporter[8681]: ts=2022-01-23T21:49:49.084Z caller=node_exporter.go:115 level=info collector=udp_queues
Jan 23 21:49:49 vagrant node_exporter[8681]: ts=2022-01-23T21:49:49.084Z caller=node_exporter.go:115 level=info collector=uname
Jan 23 21:49:49 vagrant node_exporter[8681]: ts=2022-01-23T21:49:49.084Z caller=node_exporter.go:115 level=info collector=vmstat
Jan 23 21:49:49 vagrant node_exporter[8681]: ts=2022-01-23T21:49:49.084Z caller=node_exporter.go:115 level=info collector=xfs
Jan 23 21:49:49 vagrant node_exporter[8681]: ts=2022-01-23T21:49:49.084Z caller=node_exporter.go:115 level=info collector=zfs
Jan 23 21:49:49 vagrant node_exporter[8681]: ts=2022-01-23T21:49:49.084Z caller=node_exporter.go:199 level=info msg="Listening on" address=:9100
Jan 23 21:49:49 vagrant node_exporter[8681]: ts=2022-01-23T21:49:49.085Z caller=tls_config.go:195 level=info msg="TLS is disabled." http2=false
```

Посмотрим `curl`, всё ли работает:

```bash
21:50:09 with vagrant in ~/node_exporter-1.3.1.linux-amd64 at vagrant
➜ curl http://localhost:9100/metrics
# HELP go_gc_duration_seconds A summary of the pause duration of garbage collection cycles.
# TYPE go_gc_duration_seconds summary
go_gc_duration_seconds{quantile="0"} 0
go_gc_duration_seconds{quantile="0.25"} 0
go_gc_duration_seconds{quantile="0.5"} 0
go_gc_duration_seconds{quantile="0.75"} 0
go_gc_duration_seconds{quantile="1"} 0
go_gc_duration_seconds_sum 0
go_gc_duration_seconds_count 0
# HELP go_goroutines Number of goroutines that currently exist.
# TYPE go_goroutines gauge
...
```

Открываем порт в `iptables` и добавляем строчку `config.vm.network "forwarded_port", guest: 9100, host: 9100` в `Vagrantfile`:

```bash
21:59:00 with vagrant in ~ at vagrant
➜ sudo iptables -A INPUT -p tcp --dport 9100 -j ACCEPT
```

```bash
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
       config.vm.provider "virtualbox" do |v|
       v.memory = 4096
         v.cpus = 2
             v.name = "Ubuntu-20.04-Vagrant"
             v.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
       end      
       config.vm.network "forwarded_port", guest: 9100, host: 9100
end
```

Выйдем из `ssh` сессии в `Vagrant` и выполним `vagrant halt` и `vagrant up`

```bash
22:05:24 with vagrant in ~ at vagrant took 43m 3s
➜ exit
Connection to 127.0.0.1 closed.
Nikolay in vagrant
❯  vagrant halt
==> default: Attempting graceful shutdown of VM...
Nikolay in vagrant
❯  vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Checking if box 'bento/ubuntu-20.04' version '202112.19.0' is up to date...
==> default: Clearing any previously set forwarded ports...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 9100 (guest) => 9100 (host) (adapter 1)
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Running 'pre-boot' VM customizations...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default: Warning: Connection aborted. Retrying...
    default: Warning: Connection reset. Retrying...
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
==> default: Mounting shared folders...
    default: /vagrant => G:/vagrant
==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> default: flag to force provisioning. Provisioners marked to run always will still run.
```

Видим что порт прокинулся. Зайдем в виртуальную машину и проверим что сервис запустился, хотя из хост машины уже доступен по адресу `http://127.0.0.1:9100`:

![node_export](img/img001.png)

```bash
22:12:32 with vagrant in ~ at vagrant
➜ sudo systemctl status node_exporter
● node_exporter.service - Node Exporter Service
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2022-01-23 22:07:49 UTC; 4min 54s ago
   Main PID: 657 (node_exporter)
      Tasks: 5 (limit: 4617)
     Memory: 17.3M
     CGroup: /system.slice/node_exporter.service
             └─657 /usr/local/bin/node_exporter

Jan 23 22:07:49 vagrant node_exporter[657]: ts=2022-01-23T22:07:49.650Z caller=node_exporter.go:115 level=info collector=thermal_zone
Jan 23 22:07:49 vagrant node_exporter[657]: ts=2022-01-23T22:07:49.650Z caller=node_exporter.go:115 level=info collector=time
Jan 23 22:07:49 vagrant node_exporter[657]: ts=2022-01-23T22:07:49.650Z caller=node_exporter.go:115 level=info collector=timex
Jan 23 22:07:49 vagrant node_exporter[657]: ts=2022-01-23T22:07:49.650Z caller=node_exporter.go:115 level=info collector=udp_queues
Jan 23 22:07:49 vagrant node_exporter[657]: ts=2022-01-23T22:07:49.650Z caller=node_exporter.go:115 level=info collector=uname
Jan 23 22:07:49 vagrant node_exporter[657]: ts=2022-01-23T22:07:49.650Z caller=node_exporter.go:115 level=info collector=vmstat
Jan 23 22:07:49 vagrant node_exporter[657]: ts=2022-01-23T22:07:49.650Z caller=node_exporter.go:115 level=info collector=xfs
Jan 23 22:07:49 vagrant node_exporter[657]: ts=2022-01-23T22:07:49.650Z caller=node_exporter.go:115 level=info collector=zfs
Jan 23 22:07:49 vagrant node_exporter[657]: ts=2022-01-23T22:07:49.650Z caller=node_exporter.go:199 level=info msg="Listening on" address=:9100
Jan 23 22:07:49 vagrant node_exporter[657]: ts=2022-01-23T22:07:49.650Z caller=tls_config.go:195 level=info msg="TLS is disabled." http2=false
```

Давайте так же установим `Prometheus`, скачаем последнюю версию с официального сайта:

```bash
22:12:43 with vagrant in ~ at vagrant
➜ sudo wget https://github.com/prometheus/prometheus/releases/download/v2.32.1/prometheus-2.32.1.linux-amd64.tar.gz
--2022-01-23 22:16:01--  https://github.com/prometheus/prometheus/releases/download/v2.32.1/prometheus-2.32.1.linux-amd64.tar.gz
Resolving github.com (github.com)... 140.82.121.4
Connecting to github.com (github.com)|140.82.121.4|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://objects.githubusercontent.com/github-production-release-asset-2e65be/6838921/5e44242b-0c9d-4968-a583-48baf7706f37?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20220123%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220123T221449Z&X-Amz-Expires=300&X-Amz-Signature=5cd331d5e4366fc35f3f15c45260e6b7f3559a3025e3377d05d102fe84b5caa2&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=6838921&response-content-disposition=attachment%3B%20filename%3Dprometheus-2.32.1.linux-amd64.tar.gz&response-content-type=application%2Foctet-stream [following]
--2022-01-23 22:16:02--  https://objects.githubusercontent.com/github-production-release-asset-2e65be/6838921/5e44242b-0c9d-4968-a583-48baf7706f37?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20220123%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220123T221449Z&X-Amz-Expires=300&X-Amz-Signature=5cd331d5e4366fc35f3f15c45260e6b7f3559a3025e3377d05d102fe84b5caa2&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=6838921&response-content-disposition=attachment%3B%20filename%3Dprometheus-2.32.1.linux-amd64.tar.gz&response-content-type=application%2Foctet-stream
Resolving objects.githubusercontent.com (objects.githubusercontent.com)... 185.199.108.133, 185.199.109.133, 185.199.110.133, ...
Connecting to objects.githubusercontent.com (objects.githubusercontent.com)|185.199.108.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 75073989 (72M) [application/octet-stream]
Saving to: ‘prometheus-2.32.1.linux-amd64.tar.gz’

prometheus-2.32.1.linux-amd64.tar.gz          100%[================================================================================================>]  71.60M  9.66MB/s    in 7.6s

2022-01-23 22:16:10 (9.46 MB/s) - ‘prometheus-2.32.1.linux-amd64.tar.gz’ saved [75073989/75073989]
```

Создадим папки, куда скопируем файлы `prometheus`:

```bash
22:17:17 with vagrant in ~ at vagrant
➜ sudo mkdir /etc/prometheus

22:17:26 with vagrant in ~ at vagrant
➜ sudo mkdir /var/lib/prometheus
```

Распакуем архив:

```bash
22:17:38 with vagrant in ~ at vagrant
➜ tar zxvf prometheus-*.linux-amd64.tar.gz
prometheus-2.32.1.linux-amd64/
prometheus-2.32.1.linux-amd64/consoles/
prometheus-2.32.1.linux-amd64/consoles/index.html.example
prometheus-2.32.1.linux-amd64/consoles/node-cpu.html
prometheus-2.32.1.linux-amd64/consoles/node-disk.html
prometheus-2.32.1.linux-amd64/consoles/node-overview.html
prometheus-2.32.1.linux-amd64/consoles/node.html
prometheus-2.32.1.linux-amd64/consoles/prometheus-overview.html
prometheus-2.32.1.linux-amd64/consoles/prometheus.html
prometheus-2.32.1.linux-amd64/console_libraries/
prometheus-2.32.1.linux-amd64/console_libraries/menu.lib
prometheus-2.32.1.linux-amd64/console_libraries/prom.lib
prometheus-2.32.1.linux-amd64/prometheus.yml
prometheus-2.32.1.linux-amd64/LICENSE
prometheus-2.32.1.linux-amd64/NOTICE
prometheus-2.32.1.linux-amd64/prometheus
prometheus-2.32.1.linux-amd64/promtool
```

Скопируем файлы по ранее созданным путям, отдельно библиотеки, отдельно исполняемые:

```bash
22:18:09 with vagrant in ~ at vagrant took 2s
➜ cd prometheus-*.linux-amd64

22:18:43 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant
➜ sudo cp prometheus promtool /usr/local/bin/

22:19:10 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant
➜ sudo cp -r console_libraries consoles prometheus.yml /etc/prometheus
```

Создадим пользователя, под которым будет работать `prometheus`:

```bash
22:19:29 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant
➜ sudo useradd --no-create-home --shell /bin/false prometheus
```

Назначим соответствующие права на папки и файлы:

```bash
22:20:12 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant
➜ sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus

22:20:37 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant
➜ sudo chown prometheus:prometheus /usr/local/bin/{prometheus,promtool}
```

Попробуем запустить `prometheus`, видим что запуск прошел успешно, т.к. `"Server is ready to receive web requests."` :

```bash
22:22:02 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant
➜ sudo /usr/local/bin/prometheus --config.file /etc/prometheus/prometheus.yml --storage.tsdb.path /var/lib/prometheus/ --web.console.templates=/etc/prometheus/consoles --web.console.l
ibraries=/etc/prometheus/console_libraries
ts=2022-01-23T22:22:16.129Z caller=main.go:478 level=info msg="No time or size retention was set so using the default time retention" duration=15d
ts=2022-01-23T22:22:16.129Z caller=main.go:515 level=info msg="Starting Prometheus" version="(version=2.32.1, branch=HEAD, revision=41f1a8125e664985dd30674e5bdf6b683eff5d32)"
ts=2022-01-23T22:22:16.129Z caller=main.go:520 level=info build_context="(go=go1.17.5, user=root@54b6dbd48b97, date=20211217-22:08:06)"
ts=2022-01-23T22:22:16.129Z caller=main.go:521 level=info host_details="(Linux 5.4.0-91-generic #102-Ubuntu SMP Fri Nov 5 16:31:28 UTC 2021 x86_64 vagrant (none))"
ts=2022-01-23T22:22:16.129Z caller=main.go:522 level=info fd_limits="(soft=1024, hard=1048576)"
ts=2022-01-23T22:22:16.129Z caller=main.go:523 level=info vm_limits="(soft=unlimited, hard=unlimited)"
ts=2022-01-23T22:22:16.132Z caller=web.go:570 level=info component=web msg="Start listening for connections" address=0.0.0.0:9090
ts=2022-01-23T22:22:16.133Z caller=main.go:924 level=info msg="Starting TSDB ..."
ts=2022-01-23T22:22:16.134Z caller=tls_config.go:195 level=info component=web msg="TLS is disabled." http2=false
ts=2022-01-23T22:22:16.149Z caller=head.go:488 level=info component=tsdb msg="Replaying on-disk memory mappable chunks if any"
ts=2022-01-23T22:22:16.150Z caller=head.go:522 level=info component=tsdb msg="On-disk memory mappable chunks replay completed" duration=1.896µs
ts=2022-01-23T22:22:16.150Z caller=head.go:528 level=info component=tsdb msg="Replaying WAL, this may take a while"
ts=2022-01-23T22:22:16.150Z caller=head.go:599 level=info component=tsdb msg="WAL segment loaded" segment=0 maxSegment=0
ts=2022-01-23T22:22:16.150Z caller=head.go:605 level=info component=tsdb msg="WAL replay completed" checkpoint_replay_duration=27.548µs wal_replay_duration=214.245µs total_replay_duration=258.886µs
ts=2022-01-23T22:22:16.154Z caller=main.go:945 level=info fs_type=EXT4_SUPER_MAGIC
ts=2022-01-23T22:22:16.154Z caller=main.go:948 level=info msg="TSDB started"
ts=2022-01-23T22:22:16.154Z caller=main.go:1129 level=info msg="Loading configuration file" filename=/etc/prometheus/prometheus.yml
ts=2022-01-23T22:22:16.155Z caller=main.go:1166 level=info msg="Completed loading of configuration file" filename=/etc/prometheus/prometheus.yml totalDuration=785.324µs db_storage=958ns remote_storage=1.718µs web_handler=539ns query_engine=971ns scrape=260.507µs scrape_sd=40.13µs notify=24.736µs notify_sd=6.969µs rules=1.212µs
ts=2022-01-23T22:22:16.155Z caller=main.go:897 level=info msg="Server is ready to receive web requests."
```

Создадим unit-файл:

```bash
22:23:20 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant took 18s
➜ sudo nano /etc/systemd/system/prometheus.service
```

Следующего содержания:

```bash
[Unit]
Description=Prometheus Service
After=network.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
--config.file /etc/prometheus/prometheus.yml \
--storage.tsdb.path /var/lib/prometheus/ \
--web.console.templates=/etc/prometheus/consoles \
--web.console.libraries=/etc/prometheus/console_libraries
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Перечитываем конфигурацию systemd:

```bash
22:24:13 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant took 4s
➜ sudo systemctl daemon-reload
22:24:18 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant
➜ sudo systemctl enable prometheus
Created symlink /etc/systemd/system/multi-user.target.wants/prometheus.service → /etc/systemd/system/prometheus.service.
```

Подправим сбившиеся права из-зп ручного запуска:

```bash
22:24:46 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant
➜ sudo chown -R prometheus:prometheus /var/lib/prometheus
```

Запустим службу `prometheus` и проверим что старт прошел успешно:

```bash
22:25:24 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant
➜ sudo systemctl start prometheus

22:25:59 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant
➜ sudo systemctl status prometheus
● prometheus.service - Prometheus Service
     Loaded: loaded (/etc/systemd/system/prometheus.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2022-01-23 22:25:58 UTC; 15s ago
   Main PID: 2395 (prometheus)
      Tasks: 7 (limit: 4617)
     Memory: 19.3M
     CGroup: /system.slice/prometheus.service
             └─2395 /usr/local/bin/prometheus --config.file /etc/prometheus/prometheus.yml --storage.tsdb.path /var/lib/prometheus/ --web.console.templates=/etc/prometheus/consoles ->

Jan 23 22:25:59 vagrant prometheus[2395]: ts=2022-01-23T22:25:59.002Z caller=head.go:522 level=info component=tsdb msg="On-disk memory mappable chunks replay completed" duration=2.48>
Jan 23 22:25:59 vagrant prometheus[2395]: ts=2022-01-23T22:25:59.002Z caller=head.go:528 level=info component=tsdb msg="Replaying WAL, this may take a while"
Jan 23 22:25:59 vagrant prometheus[2395]: ts=2022-01-23T22:25:59.606Z caller=head.go:599 level=info component=tsdb msg="WAL segment loaded" segment=0 maxSegment=1
Jan 23 22:25:59 vagrant prometheus[2395]: ts=2022-01-23T22:25:59.606Z caller=head.go:599 level=info component=tsdb msg="WAL segment loaded" segment=1 maxSegment=1
Jan 23 22:25:59 vagrant prometheus[2395]: ts=2022-01-23T22:25:59.606Z caller=head.go:605 level=info component=tsdb msg="WAL replay completed" checkpoint_replay_duration=36.42µs wal_r>
Jan 23 22:25:59 vagrant prometheus[2395]: ts=2022-01-23T22:25:59.607Z caller=main.go:945 level=info fs_type=EXT4_SUPER_MAGIC
Jan 23 22:25:59 vagrant prometheus[2395]: ts=2022-01-23T22:25:59.607Z caller=main.go:948 level=info msg="TSDB started"
Jan 23 22:25:59 vagrant prometheus[2395]: ts=2022-01-23T22:25:59.607Z caller=main.go:1129 level=info msg="Loading configuration file" filename=/etc/prometheus/prometheus.yml
Jan 23 22:25:59 vagrant prometheus[2395]: ts=2022-01-23T22:25:59.608Z caller=main.go:1166 level=info msg="Completed loading of configuration file" filename=/etc/prometheus/prometheus>
Jan 23 22:25:59 vagrant prometheus[2395]: ts=2022-01-23T22:25:59.608Z caller=main.go:897 level=info msg="Server is ready to receive web requests."
lines 1-19/19 (END)
```

Открываем порт в `iptables` и добавляем строчку `config.vm.network "forwarded_port", guest: 9090, host: 9090` в `Vagrantfile`:

```bash
22:28:03 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant took 1m 49s
➜ sudo iptables -A INPUT -p tcp --dport 9090 -j ACCEPT
```

```bash
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
       config.vm.provider "virtualbox" do |v|
       v.memory = 4096
         v.cpus = 2
             v.name = "Ubuntu-20.04-Vagrant"
             v.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
       end      
       config.vm.network "forwarded_port", guest: 9100, host: 9100
       config.vm.network "forwarded_port", guest: 9090, host: 9090
end
```

Внесем изменения в конфиг `prometheus`, чтобы он брал данные из `127.0.0.1:9100`, т.е. `node_export`:

```bash
22:28:05 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant
➜ sudo nano /etc/prometheus/prometheus.yml
```

```bash
  - job_name: 'node_exporter_clients'
    scrape_interval: 5s
    static_configs:
      - targets: ['127.0.0.1:9100']
```

Перезагрузим `prometheus` для применения данных из конфига:

```bash
22:31:28 with vagrant in ~/prometheus-2.32.1.linux-amd64 at vagrant took 1m 49s
➜ sudo systemctl restart prometheus
```

Выйдем из `ssh` сессии в `Vagrant` и выполним `vagrant halt` и `vagrant up`:

```bash
Nikolay in vagrant
❯  vagrant halt
==> default: Attempting graceful shutdown of VM...
Nikolay in vagrant
❯  vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Checking if box 'bento/ubuntu-20.04' version '202112.19.0' is up to date...
==> default: Clearing any previously set forwarded ports...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 9100 (guest) => 9100 (host) (adapter 1)
    default: 9090 (guest) => 9090 (host) (adapter 1)
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Running 'pre-boot' VM customizations...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
==> default: Mounting shared folders...
    default: /vagrant => G:/vagrant
==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> default: flag to force provisioning. Provisioners marked to run always will still run.
Nikolay in vagrant
❯  vagrant ssh
```

Видим `Prometheus` успешно работает.

![Prometheus](img/img002.png)

#### 2. Ознакомьтесь с опциями node_exporter и выводом `/metrics` по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.

Для начала изучим что есть, вызовем `curl http://localhost:9100/metrics`, вывод будет большим, выбираем `node_cpu` а так же один параметр из `cpu`, `node_disk`, `node_memory` и `node_network` 

##### CPU

```bash
22:53:42 with vagrant in ~ at vagrant took 14m 47s
➜ curl http://localhost:9100/metrics | grep node_cpu
```
 
Total user and system CPU time spent in seconds

- process_cpu_seconds_total 3.53

Seconds the CPUs spent in each mode.

- node_cpu_seconds_total{cpu="0",mode="idle"} 1137.04
- node_cpu_seconds_total{cpu="0",mode="system"} 7.11
- node_cpu_seconds_total{cpu="0",mode="user"} 4.46

Соответственно по кол-ву CPU.

```bash
22:54:13 with vagrant in ~ at vagrant
➜ curl http://localhost:9100/metrics | grep node_memory
```

##### MEMORY

Memory information field Cached_bytes.

- node_memory_Cached_bytes 5.84380416e+08

Memory information field Active_bytes.

- node_memory_Active_bytes 3.1062016e+08

Memory information field MemAvailable_bytes.

- node_memory_MemAvailable_bytes 3.705700352e+09

Memory information field MemFree_bytes.

- node_memory_MemFree_bytes 3.251535872e+09

```bash
23:06:29 with vagrant in ~ at vagrant
➜ curl http://localhost:9100/metrics | grep node_disk
```

##### DISK

The number of I/Os currently in progress.

- node_disk_io_now{device="sda"} 0

Total seconds spent doing I/Os.

- node_disk_io_time_seconds_total{device="sda"} 20.092

The total number of bytes read successfully.

- node_disk_read_bytes_total{device="sda"} 5.40719104e+08

The total number of seconds spent by all reads.

- node_disk_read_time_seconds_total{device="sda"} 26.657

This is the total number of seconds spent by all writes.

- node_disk_write_time_seconds_total{device="sda"} 2.259

The total number of bytes written successfully.

- node_disk_written_bytes_total{device="sda"} 3.0916608e+07

```bash
23:11:50 with vagrant in ~ at vagrant
➜ curl http://localhost:9100/metrics | grep node_network
```

##### NETWORK

Network device statistic receive_bytes.

- node_network_receive_bytes_total{device="eth0"} 1.310313e+06

Network device statistic receive_drop.

- node_network_receive_drop_total{device="eth0"} 0

Network device statistic receive_errs.

- node_network_receive_errs_total{device="eth0"} 0

Network device statistic receive_packets.

- node_network_receive_packets_total{device="eth0"} 5384

Network device statistic transmit_bytes.

- node_network_transmit_bytes_total{device="eth0"} 3.539839e+06

Network device statistic transmit_drop.

- node_network_transmit_drop_total{device="eth0"} 0

Network device statistic transmit_errs.

- node_network_transmit_errs_total{device="eth0"} 0


Network device statistic transmit_packets.

- node_network_transmit_packets_total{device="eth0"} 4292

#### 3. Установите в свою виртуальную машину [Netdata](https://github.com/netdata/netdata). Воспользуйтесь [готовыми пакетами](https://packagecloud.io/netdata/netdata/install) для установки (`sudo apt install -y netdata`). После успешной установки:
    * в конфигурационном файле `/etc/netdata/netdata.conf` в секции [web] замените значение с localhost на `bind to = 0.0.0.0`,
    * добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте `vagrant reload`:

```bash
    config.vm.network "forwarded_port", guest: 19999, host: 19999
```

####     После успешной перезагрузки в браузере *на своем ПК* (не в виртуальной машине) вы должны суметь зайти на `localhost:19999`. Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.

Устанавливаем `netdata`:

```bash
23:26:20 with vagrant in ~ at vagrant took 29s
➜ sudo apt install -y netdata
```

Правим конфиг:

```bash
23:26:20 with vagrant in ~ at vagrant took 29s
➜ nano /etc/netdata/netdata.conf
```

```bash
# NetData Configuration

# The current full configuration can be retrieved from the running
# server at the URL
#
#   http://localhost:19999/netdata.conf
#
# for example:
#
#   wget -O /etc/netdata/netdata.conf http://localhost:19999/netdata.conf
#

[global]
        run as user = netdata
        web files owner = root
        web files group = root
        # Netdata is not designed to be exposed to potentially hostile
        # networks. See https://github.com/netdata/netdata/issues/164
        bind socket to IP = 0.0.0.0
```

Добавляем строчку `config.vm.network "forwarded_port", guest: 19999, host: 19999` в `Vagrantfile` и выполняем `vagrant reload`:

```bash
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
       config.vm.provider "virtualbox" do |v|
       v.memory = 4096
         v.cpus = 2
             v.name = "Ubuntu-20.04-Vagrant"
             v.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
       end      
       config.vm.network "forwarded_port", guest: 9100, host: 9100
       config.vm.network "forwarded_port", guest: 9090, host: 9090
       config.vm.network "forwarded_port", guest: 19999, host: 19999
end
```

После перезапуска `netdata` доступна из хост системы:

![netdata](img/img003.png)

#### 4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?

Да, можно:

```bash
23:40:51 with vagrant in ~ at vagrant
➜ dmesg | head -30
[    0.000000] Linux version 5.4.0-91-generic (buildd@lcy01-amd64-017) (gcc version 9.3.0 (Ubuntu 9.3.0-17ubuntu1~20.04)) #102-Ubuntu SMP Fri Nov 5 16:31:28 UTC 2021 (Ubuntu 5.4.0-91.102-generic 5.4.151)
[    0.000000] Command line: BOOT_IMAGE=/vmlinuz-5.4.0-91-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro net.ifnames=0 biosdevname=0
[    0.000000] KERNEL supported cpus:
[    0.000000]   Intel GenuineIntel
[    0.000000]   AMD AuthenticAMD
[    0.000000]   Hygon HygonGenuine
[    0.000000]   Centaur CentaurHauls
[    0.000000]   zhaoxin   Shanghai
[    0.000000] x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'
[    0.000000] x86/fpu: Supporting XSAVE feature 0x002: 'SSE registers'
[    0.000000] x86/fpu: Supporting XSAVE feature 0x004: 'AVX registers'
[    0.000000] x86/fpu: xstate_offset[2]:  576, xstate_sizes[2]:  256
[    0.000000] x86/fpu: Enabled xstate features 0x7, context size is 832 bytes, using 'standard' format.
[    0.000000] BIOS-provided physical RAM map:
[    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable
[    0.000000] BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000000f0000-0x00000000000fffff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000000100000-0x00000000dffeffff] usable
[    0.000000] BIOS-e820: [mem 0x00000000dfff0000-0x00000000dfffffff] ACPI data
[    0.000000] BIOS-e820: [mem 0x00000000fec00000-0x00000000fec00fff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000fee00000-0x00000000fee00fff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000fffc0000-0x00000000ffffffff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000100000000-0x000000011fffffff] usable
[    0.000000] NX (Execute Disable) protection: active
[    0.000000] SMBIOS 2.5 present.
[    0.000000] DMI: innotek GmbH VirtualBox/VirtualBox, BIOS VirtualBox 12/01/2006
[    0.000000] Hypervisor detected: KVM
[    0.000000] kvm-clock: Using msrs 4b564d01 and 4b564d00
[    0.000000] kvm-clock: cpu 0, msr 116e01001, primary cpu clock
[    0.000000] kvm-clock: using sched offset of 6555150697 cycles

23:40:54 with vagrant in ~ at vagrant
➜ dmesg | grep virtual
[    0.001646] CPU MTRRs all blank - virtualized system.
[    0.393580] Booting paravirtualized kernel on KVM
[    4.752554] systemd[1]: Detected virtualization oracle.

23:41:20 with vagrant in ~ at vagrant
➜ dmesg | grep KVM
[    0.000000] Hypervisor detected: KVM
[    0.393580] Booting paravirtualized kernel on KVM
```

#### 5. Как настроен sysctl `fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)?

Это обозначает максимальное количество файловых дескрипторов, которые может выделить процесс.

По умолчанию:

```bash
23:42:36 with vagrant in ~ at vagrant
➜ /sbin/sysctl -n fs.nr_open
1048576
```

Не позволит достичь:

  `-n`   The maximum number of open file descriptors. 

```bash
23:48:09 with vagrant in ~ at vagrant took 47s
➜ ulimit -n
1024
```


#### 6. Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через `nsenter`. Для простоты работайте в данном задании под root (`sudo -i`). Под обычным пользователем требуются дополнительные опции (`--map-root-user`) и т.д.

Перейдем под рута `sudo -i`

Запустим `screen`. Поделим экран пополам - `ctrl+a` + `S`, `ctrl+a` + `TAB`, `ctrl+a` + `c`.

В верхней части выполним:

```bash
root@vagrant:~# unshare -f --pid --mount-proc sleep 1h &
[1] 2663
root@vagrant:~#
```

![unshare](img/img004.png)

Затем `ps aux` и выясним что `pid` нужного процесса `2664`:

```bash
root        2267  0.0  0.0      0     0 ?        I    Jan23   0:00 [kworker/u4:1-events_power_efficient]
root        2564  0.0  0.0      0     0 ?        R    Jan23   0:00 [kworker/u4:2-events_unbound]
root        2620  0.0  0.1   9264  4560 pts/0    S    Jan23   0:00 sudo -i
root        2622  0.0  0.1   7236  4172 pts/0    S    Jan23   0:00 -bash
root        2634  0.0  0.0   6820  2972 pts/0    S+   Jan23   0:00 screen -S test
root        2635  0.0  0.0   7416  2936 ?        Rs   Jan23   0:00 SCREEN -S test
root        2636  0.0  0.1   7496  4228 pts/1    Ss   Jan23   0:00 /bin/bash
root        2647  0.0  0.0   7236  3920 pts/2    Ss+  Jan23   0:00 /bin/bash
root        2661  0.0  0.0      0     0 ?        I    Jan23   0:00 [kworker/u4:0-events_unbound]
root        2663  0.0  0.0   5480   592 pts/1    S    Jan23   0:00 unshare -f --pid --mount-proc sleep 1h
root        2664  0.0  0.0   5476   592 pts/1    S    Jan23   0:00 sleep 1h
root        2676  0.0  0.0      0     0 ?        I    00:00   0:00 [kworker/1:1-events]
root        2693  0.0  0.0      0     0 ?        I    00:00   0:00 [kworker/0:0-events]
root        2694  0.0  0.0      0     0 ?        I    00:00   0:00 [kworker/0:2-events]
root        2695  0.0  0.0      0     0 ?        I    00:00   0:00 [kworker/1:3-cgroup_destroy]
root        2696  0.0  0.0      0     0 ?        I    00:00   0:00 [kworker/0:4]
root        2727  0.0  0.0   8892  3176 pts/1    R+   00:04   0:00 ps aux
root@vagrant:~#
```

В нижней части выполним:

```bash
root@vagrant:~# nsenter --target 2664 --pid --mount
root@vagrant:/# ps aux | grep sleep
root           1  0.0  0.0   5476   592 pts/1    S+   Jan23   0:00 sleep 1h
root          14  0.0  0.0   6432   664 pts/2    S+   00:04   0:00 grep --color=auto sleep
root@vagrant:/#
```

![nsenter](img/img005.png)

Как видим наш процесс работает под `pid 1`.

#### 7. Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 (**это важно, поведение в других ОС не проверялось**). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. Вызов `dmesg` расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?

Выполнил, всё зависло:

```bash
00:11:11 with vagrant in ~ at vagrant
➜ :(){ :|:& };:
[2] 2871 2872
[2]  + 2871 done       : |
       2872 done       :
```

```bash
bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
```

```bash
[   47.383827] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-3.scope
[1]+  Done                    : | :
```
Судя по всему это форк-бомба, о которой упоминалось на лекции, а именно на языке `bash`

```bash
:()       # Определение функции
  {       # Открытие функции
    :|:&  # Далее, загружает копию функции «:» в память тем самым, будет вызывать само себя с использованием техники программирования ( так называемая рекурсия) и передает результат на другой вызов функции. ‘:’ — Худшая часть — функция, вызываемая два раза, чтобы «бомбить» вашу систему. & — Помещает вызов функции в фоновом режиме, чтобы fork (дочерний процесс) не мог «умереть» вообще, тем самым это начнет есть системные ресурсы
  }       # Закрытие функции
  ;       # Завершите определение функции. 
:         # Запускает функцию которая порождает fork bomb().
```
Функция с именем `:` которая дважды вызывает сама себя.

Так же информация о ней есть на [Википедии](https://ru.wikipedia.org/wiki/Fork-%D0%B1%D0%BE%D0%BC%D0%B1%D0%B0)  

Восстанавливает жизнеспособность системы:

```bash
01:02:57 with vagrant in ~ at vagrant
➜ dmesg | grep fork
[   47.383827] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-3.scope
```

Число процессов указано в ulimit -u:

```bash
00:59:15 with vagrant in ~ at vagrant
➜ ulimit -u
3571
```



 ---

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в [Google Docs](https://docs.google.com/document/u/0/?tgif=d) и отправить в личном кабинете на проверку ссылку на ваш документ.
Название файла Google Docs должно содержать номер лекции и фамилию студента. Пример названия: "1.1. Введение в DevOps — Сусанна Алиева".

Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу. Чтобы это проверить, откройте ссылку в браузере в режиме инкогнито.

[Как предоставить доступ к файлам и папкам на Google Диске](https://support.google.com/docs/answer/2494822?hl=ru&co=GENIE.Platform%3DDesktop)

[Как запустить chrome в режиме инкогнито ](https://support.google.com/chrome/answer/95464?co=GENIE.Platform%3DDesktop&hl=ru)

[Как запустить  Safari в режиме инкогнито ](https://support.apple.com/ru-ru/guide/safari/ibrw1069/mac)

Любые вопросы по решению задач задавайте в чате учебной группы.

---

