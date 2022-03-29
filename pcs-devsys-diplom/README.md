# Курсовая работа по итогам модуля "DevOps и системное администрирование"

Курсовая работа необходима для проверки практических навыков, полученных в ходе прохождения курса "DevOps и системное администрирование".

Мы создадим и настроим виртуальное рабочее место. Позже вы сможете использовать эту систему для выполнения домашних заданий по курсу

## Задание

---

1. Создайте виртуальную машину Linux.

---

Запускаем виртуальную машину в VB через Vagrant:

```bash
Nikolay in course_work
❯  vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Checking if box 'bento/ubuntu-20.04' version '202112.19.0' is up to date...
==> default: Clearing any previously set forwarded ports...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
    default: 443 (guest) => 1443 (host) (adapter 1)
==> default: Running 'pre-boot' VM customizations...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default: Warning: Connection reset. Retrying...
    default: Warning: Connection aborted. Retrying...
    default: Warning: Remote connection disconnect. Retrying...
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
==> default: Mounting shared folders...
    default: /vagrant => G:/course_work
==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> default: flag to force provisioning. Provisioners marked to run always will still run.
Nikolay in course_work
❯
```

---

2. Установите ufw и разрешите к этой машине сессии на порты 22 и 443, при этом трафик на интерфейсе localhost (lo) должен ходить свободно на все порты.

---

Сбросим правила `ufw`:

```bash
vagrant@vagrant:~$ sudo ufw default deny incoming
Default incoming policy changed to 'deny'
(be sure to update your rules accordingly)
vagrant@vagrant:~$ sudo ufw default allow outgoing
Default outgoing policy changed to 'allow'
(be sure to update your rules accordingly)
```

Откроем доступ по ssh (22), https (443):

```bash
vagrant@vagrant:~$ sudo ufw allow ssh
Rules updated
Rules updated (v6)
vagrant@vagrant:~$
vagrant@vagrant:~$ sudo ufw allow https
Rules updated
Rules updated (v6)
```

Активируем `ufw`, нас предупреждают что ssh соединение порвется:

```bash
vagrant@vagrant:~$ sudo ufw enable
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup
```

Проверим заданные правила:

```bash
vagrant@vagrant:~$ sudo ufw status verbose
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere
22/tcp (v6)                ALLOW IN    Anywhere (v6)
443/tcp (v6)               ALLOW IN    Anywhere (v6)
```
---

3. Установите hashicorp vault ([инструкция по ссылке](https://learn.hashicorp.com/tutorials/vault/getting-started-install?in=vault/getting-started#install-vault)).

---
С установкой возникли трудности, т.к. с ip адреса РФ запрещен доступ к скачиванию с сайта и репозитория HashiCorp, для этого пришлось использовать Gateway от Whonix. Поднял второй сетевой адаптер на виртуальной машине, указал его как шлюз для дефолтных маршрутов.

Добавим HashiCorp GPG key.

```bash
vagrant@vagrant:~$ curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
OK
```

Добавим официальный HashiCorp Linux репозиторий.

```bash
vagrant@vagrant:~$ sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
Hit:1 http://us.archive.ubuntu.com/ubuntu focal InRelease
Get:2 http://us.archive.ubuntu.com/ubuntu focal-updates InRelease [114 kB]
Get:3 https://apt.releases.hashicorp.com focal InRelease [15.4 kB]
Get:4 https://apt.releases.hashicorp.com focal/main amd64 Packages [50.7 kB]
Get:5 http://us.archive.ubuntu.com/ubuntu focal-backports InRelease [108 kB]
Get:6 http://us.archive.ubuntu.com/ubuntu focal-security InRelease [114 kB]
Get:7 http://us.archive.ubuntu.com/ubuntu focal-updates/main amd64 Packages [1,674 kB]
Fetched 2,076 kB in 5s (461 kB/s)
Reading package lists... Done
```

Обновим информацию о пакетах и установим HashiCorp Vault.

```bash
vagrant@vagrant:~$ sudo apt-get update && sudo apt-get install vault
Hit:1 http://us.archive.ubuntu.com/ubuntu focal InRelease
Hit:2 http://us.archive.ubuntu.com/ubuntu focal-updates InRelease
Hit:3 https://apt.releases.hashicorp.com focal InRelease
Hit:4 http://us.archive.ubuntu.com/ubuntu focal-backports InRelease
Hit:5 http://us.archive.ubuntu.com/ubuntu focal-security InRelease
Reading package lists... Done
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following package was automatically installed and is no longer required:
  libfwupdplugin1
Use 'sudo apt autoremove' to remove it.
The following NEW packages will be installed:
  vault
0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
Need to get 70.4 MB of archives.
After this operation, 191 MB of additional disk space will be used.
Get:1 https://apt.releases.hashicorp.com focal/main amd64 vault amd64 1.10.0 [70.4 MB]
Fetched 70.4 MB in 1min 1s (1,158 kB/s)
Selecting previously unselected package vault.
(Reading database ... 47655 files and directories currently installed.)
Preparing to unpack .../vault_1.10.0_amd64.deb ...
Unpacking vault (1.10.0) ...
Setting up vault (1.10.0) ...
Generating Vault TLS key and self-signed certificate...
Generating a RSA private key
......................................................................................................................................................................++++
........................................................................++++
writing new private key to 'tls.key'
-----
Vault TLS key and self-signed certificate have been generated in '/opt/vault/tls'.
```

Проверим установку:

```bash
vagrant@vagrant:~$ vault
Usage: vault <command> [args]

Common commands:
    read        Read data and retrieves secrets
    write       Write data, configuration, and secrets
    delete      Delete secrets and configuration
    list        List data or secrets
    login       Authenticate locally
    agent       Start a Vault agent
    server      Start a Vault server
    status      Print seal and HA status
    unwrap      Unwrap a wrapped secret

Other commands:
    audit                Interact with audit devices
    auth                 Interact with auth methods
    debug                Runs the debug command
    kv                   Interact with Vault's Key-Value storage
    lease                Interact with leases
    monitor              Stream log messages from a Vault server
    namespace            Interact with namespaces
    operator             Perform operator-specific tasks
    path-help            Retrieve API help for paths
    plugin               Interact with Vault plugins and catalog
    policy               Interact with policies
    print                Prints runtime configurations
    secrets              Interact with secrets engines
    ssh                  Initiate an SSH session
    token                Interact with tokens
    version-history      Prints the version history of the target Vault server
```

---

4. Cоздайте центр сертификации по инструкции ([ссылка](https://learn.hashicorp.com/tutorials/vault/pki-engine?in=vault/secrets-management)) и выпустите сертификат для использования его в настройке веб-сервера nginx (срок жизни сертификата - месяц).

---

Установим jq:

```bash
vagrant@vagrant:~$ sudo apt-get install jq
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following package was automatically installed and is no longer required:
  libfwupdplugin1
Use 'sudo apt autoremove' to remove it.
The following additional packages will be installed:
  libjq1 libonig5
The following NEW packages will be installed:
  jq libjq1 libonig5
0 upgraded, 3 newly installed, 0 to remove and 0 not upgraded.
Need to get 313 kB of archives.
After this operation, 1,062 kB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://us.archive.ubuntu.com/ubuntu focal/universe amd64 libonig5 amd64 6.9.4-1 [142 kB]
Get:2 http://us.archive.ubuntu.com/ubuntu focal-updates/universe amd64 libjq1 amd64 1.6-1ubuntu0.20.04.1 [121 kB]
Get:3 http://us.archive.ubuntu.com/ubuntu focal-updates/universe amd64 jq amd64 1.6-1ubuntu0.20.04.1 [50.2 kB]
Fetched 313 kB in 2s (171 kB/s)
Selecting previously unselected package libonig5:amd64.
(Reading database ... 47661 files and directories currently installed.)
Preparing to unpack .../libonig5_6.9.4-1_amd64.deb ...
Unpacking libonig5:amd64 (6.9.4-1) ...
Selecting previously unselected package libjq1:amd64.
Preparing to unpack .../libjq1_1.6-1ubuntu0.20.04.1_amd64.deb ...
Unpacking libjq1:amd64 (1.6-1ubuntu0.20.04.1) ...
Selecting previously unselected package jq.
Preparing to unpack .../jq_1.6-1ubuntu0.20.04.1_amd64.deb ...
Unpacking jq (1.6-1ubuntu0.20.04.1) ...
Setting up libonig5:amd64 (6.9.4-1) ...
Setting up libjq1:amd64 (1.6-1ubuntu0.20.04.1) ...
Setting up jq (1.6-1ubuntu0.20.04.1) ...
Processing triggers for man-db (2.9.1-1) ...
Processing triggers for libc-bin (2.31-0ubuntu9.7) ...
```

Настраиваем политики согласно [инструкции](https://learn.hashicorp.com/tutorials/vault/policies).

Запускаем сервер vault в dev режиме в отдельной сессии:

```bash
vagrant@vagrant:~$ vault server -dev -dev-root-token-id=root
==> Vault server configuration:

             Api Address: http://127.0.0.1:8200
                     Cgo: disabled
         Cluster Address: https://127.0.0.1:8201
              Go Version: go1.17.7
              Listener 1: tcp (addr: "127.0.0.1:8200", cluster address: "127.0.0.1:8201", max_request_duration: "1m30s", max_request_size: "33554432", tls: "disabled")
               Log Level: info
                   Mlock: supported: true, enabled: false
           Recovery Mode: false
                 Storage: inmem
                 Version: Vault v1.10.0
             Version Sha: 7738ec5d0d6f5bf94a809ee0f6ff0142cfa525a6

==> Vault server started! Log data will stream in below:

2022-03-27T21:05:43.793Z [INFO]  proxy environment: http_proxy="" https_proxy="" no_proxy=""
2022-03-27T21:05:43.793Z [WARN]  no `api_addr` value specified in config or in VAULT_API_ADDR; falling back to detection if possible, but this value should be manually set
2022-03-27T21:05:43.793Z [INFO]  core: Initializing versionTimestamps for core
2022-03-27T21:05:43.800Z [INFO]  core: security barrier not initialized
2022-03-27T21:05:43.800Z [INFO]  core: security barrier initialized: stored=1 shares=1 threshold=1
2022-03-27T21:05:43.800Z [INFO]  core: post-unseal setup starting
2022-03-27T21:05:43.803Z [INFO]  core: loaded wrapping token key
2022-03-27T21:05:43.803Z [INFO]  core: Recorded vault version: vault version=1.10.0 upgrade time="2022-03-27 21:05:43.803440664 +0000 UTC"
2022-03-27T21:05:43.803Z [INFO]  core: successfully setup plugin catalog: plugin-directory=""
2022-03-27T21:05:43.803Z [INFO]  core: no mounts; adding default mount table
2022-03-27T21:05:43.804Z [INFO]  core: successfully mounted backend: type=cubbyhole path=cubbyhole/
2022-03-27T21:05:43.805Z [INFO]  core: successfully mounted backend: type=system path=sys/
2022-03-27T21:05:43.805Z [INFO]  core: successfully mounted backend: type=identity path=identity/
2022-03-27T21:05:43.815Z [INFO]  core: successfully enabled credential backend: type=token path=token/
2022-03-27T21:05:43.815Z [INFO]  rollback: starting rollback manager
2022-03-27T21:05:43.816Z [INFO]  core: restoring leases
2022-03-27T21:05:43.816Z [INFO]  expiration: lease restore complete
2022-03-27T21:05:43.816Z [INFO]  identity: entities restored
2022-03-27T21:05:43.816Z [INFO]  identity: groups restored
2022-03-27T21:05:44.575Z [INFO]  core: post-unseal setup complete
2022-03-27T21:05:44.575Z [INFO]  core: root token generated
2022-03-27T21:05:44.575Z [INFO]  core: pre-seal teardown starting
2022-03-27T21:05:44.575Z [INFO]  rollback: stopping rollback manager
2022-03-27T21:05:44.575Z [INFO]  core: pre-seal teardown complete
2022-03-27T21:05:44.617Z [INFO]  core.cluster-listener.tcp: starting listener: listener_address=127.0.0.1:8201
2022-03-27T21:05:44.617Z [INFO]  core.cluster-listener: serving cluster requests: cluster_listen_address=127.0.0.1:8201
2022-03-27T21:05:44.617Z [INFO]  core: post-unseal setup starting
2022-03-27T21:05:44.620Z [INFO]  core: loaded wrapping token key
2022-03-27T21:05:44.620Z [INFO]  core: successfully setup plugin catalog: plugin-directory=""
2022-03-27T21:05:44.620Z [INFO]  core: successfully mounted backend: type=system path=sys/
2022-03-27T21:05:44.620Z [INFO]  core: successfully mounted backend: type=identity path=identity/
2022-03-27T21:05:44.620Z [INFO]  core: successfully mounted backend: type=cubbyhole path=cubbyhole/
2022-03-27T21:05:44.621Z [INFO]  core: successfully enabled credential backend: type=token path=token/
2022-03-27T21:05:44.621Z [INFO]  core: restoring leases
2022-03-27T21:05:44.621Z [INFO]  rollback: starting rollback manager
2022-03-27T21:05:44.622Z [INFO]  expiration: lease restore complete
2022-03-27T21:05:44.622Z [INFO]  identity: entities restored
2022-03-27T21:05:44.622Z [INFO]  identity: groups restored
2022-03-27T21:05:44.622Z [INFO]  core: post-unseal setup complete
2022-03-27T21:05:44.622Z [INFO]  core: vault is unsealed
2022-03-27T21:05:44.623Z [INFO]  expiration: revoked lease: lease_id=auth/token/root/h3efb09c2d27a1ae9f4bf44c51ad5b87aae526e9703959b88e04ee9b084ac4990
2022-03-27T21:05:44.626Z [INFO]  core: successful mount: namespace="" path=secret/ type=kv
2022-03-27T21:05:44.674Z [INFO]  secrets.kv.kv_6d08aa79: collecting keys to upgrade
2022-03-27T21:05:44.674Z [INFO]  secrets.kv.kv_6d08aa79: done collecting keys: num_keys=1
2022-03-27T21:05:44.674Z [INFO]  secrets.kv.kv_6d08aa79: upgrading keys finished
WARNING! dev mode is enabled! In this mode, Vault runs entirely in-memory
and starts unsealed with a single unseal key. The root token is already
authenticated to the CLI, so you can immediately begin using Vault.

You may need to set the following environment variable:

    $ export VAULT_ADDR='http://127.0.0.1:8200'

The unseal key and root token are displayed below in case you want to
seal/unseal the Vault or re-authenticate.

Unseal Key: Das1j9VtsUGUQ3WxX/4mWoXlZoKElh8wK3GCzT/6CEY=
Root Token: root

Development mode should NOT be used in production installations!
```

В основной сессии делаем экспорт переменных среды:

```bash
vagrant@vagrant:~$ export VAULT_ADDR=http://127.0.0.1:8200 # - Export an environment variable for the vault CLI to address the Vault server.
vagrant@vagrant:~$ export VAULT_TOKEN=root # - Export an environment variable for the vault CLI to authenticate with the Vault server.
```

Далее создаем файл с политикой:

```bash
tee admin-policy.hcl <<EOF # Define the admin policy in the file named admin-policy.hcl.
# Read system health check
path "sys/health"
{
  capabilities = ["read", "sudo"]
}

# Create and manage ACL policies broadly across Vault

# List existing policies
path "sys/policies/acl"
{
  capabilities = ["list"]
}

# Create and manage ACL policies
path "sys/policies/acl/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Enable and manage authentication methods broadly across Vault

# Manage auth methods broadly across Vault
path "auth/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Create, update, and delete auth methods
path "sys/auth/*"
{
  capabilities = ["read","create", "update", "delete", "sudo"]
}

# List auth methods
path "sys/auth"
{
  capabilities = ["read"]
}

# Enable and manage the key/value secrets engine at  path

# List, create, update, and delete key/value secrets
path "secret/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Manage secrets engines
path "sys/mounts/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# List enabled secrets engine
path "sys/mounts" {
  capabilities = [ "read", "list" ]
}

# Work with pki secrets engine
path "pki*" {
  capabilities = [ "create", "read", "update", "delete", "list", "sudo" ]
}
EOF
```

И создаем политику admin на сервере

```bash
vagrant@vagrant:~$ vault policy write admin admin-policy.hcl # Create a policy named admin with the policy defined in admin-policy.hcl.
Success! Uploaded policy: admin
```

Проверим что всё создалось:

```bash
vagrant@vagrant:~$ vault policy list # List all the policies.
admin
default
root
```

Прочтем политику admin:

```bash
vagrant@vagrant:~$ vault policy read admin # Read the admin policy.
# Read system health check
path "sys/health"
{
  capabilities = ["read", "sudo"]
}

# Create and manage ACL policies broadly across Vault

# List existing policies
path "sys/policies/acl"
{
  capabilities = ["list"]
}

# Create and manage ACL policies
path "sys/policies/acl/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Enable and manage authentication methods broadly across Vault

# Manage auth methods broadly across Vault
path "auth/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Create, update, and delete auth methods
path "sys/auth/*"
{
  capabilities = ["read","create", "update", "delete", "sudo"]
}

# List auth methods
path "sys/auth"
{
  capabilities = ["read"]
}

# Enable and manage the key/value secrets engine at  path

# List, create, update, and delete key/value secrets
path "secret/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Manage secrets engines
path "sys/mounts/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# List enabled secrets engine
path "sys/mounts" {
  capabilities = [ "read", "list" ]
}

# Work with pki secrets engine
path "pki*" {
  capabilities = [ "create", "read", "update", "delete", "list", "sudo" ]
}
```

Создадим токен с политикой админ и поместим в переменную ADMIN_TOKEN

```bash
vagrant@vagrant:~$ ADMIN_TOKEN=$(vault token create -format=json -policy="admin" | jq -r ".auth.client_token") # Create a token with the admin policy attached and store the token in the variable ADMIN_TOKEN.
```

Выведем содержимое ADMIN_TOKEN, чтобы проверить что всё успешно:

```bash
vagrant@vagrant:~$ echo $ADMIN_TOKEN # Display the ADMIN_TOKEN.
hvs.CAESIPzof01SRMzyTLVVuVR1aZwxmszb-J6T9jJpLqmvKKGeGh4KHGh2cy5oRkhySFpSaFNXa0NvRkx2aUdWZU5pWGQ
```

Проверим права на путь sys/auth/approle:

```bash
vagrant@vagrant:~$ vault token capabilities $ADMIN_TOKEN sys/auth/approle
create, delete, read, sudo, update
```

Проверим права на путь не описанный в политике:

```bash
vagrant@vagrant:~$ vault token capabilities $ADMIN_TOKEN identity/entity # Retrieve the capabilities of this token for a path not defined in the policy.
deny
```

Шаг 1. Создать корневой центр сертификации и сгенерировать корневой сертификат.

На этом шаге мы собираемся сгенерировать самозаверяющий корневой сертификат с помощью PKI secrets engine.

![1](img/img001.PNG)

```bash
vagrant@vagrant:~$ vault secrets enable pki
Success! Enabled the pki secrets engine at: pki/
```

Настраиваем secrets engine pki на выдачу сертификатов с максимальным сроком службы (TTL) 87600 часов.

```bash
vagrant@vagrant:~$ vault secrets tune -max-lease-ttl=87600h pki
Success! Tuned the secrets engine at: pki/
```

Создаем корневой сертификат и сохраняем его в CA_cert.crt.

```bash
vagrant@vagrant:~$ vault write -field=certificate pki/root/generate/internal common_name="example.com" ttl=87600h > CA_cert.crt
```

Проверим что сгенерировалось:

```bash
vagrant@vagrant:~$ cat CA_cert.crt
-----BEGIN CERTIFICATE-----
MIIDNTCCAh2gAwIBAgIUXcBjJi4vwX2h6V/vyliS59fxoOEwDQYJKoZIhvcNAQEL
BQAwFjEUMBIGA1UEAxMLZXhhbXBsZS5jb20wHhcNMjIwMzI3MjE0OTE4WhcNMzIw
MzI0MjE0OTQ4WjAWMRQwEgYDVQQDEwtleGFtcGxlLmNvbTCCASIwDQYJKoZIhvcN
AQEBBQADggEPADCCAQoCggEBANJObifuPQQoQ7/rlFW1rk3jWWUmcCCnd6BzVpAe
WAXz/gV0DcKm9YsTCFkV9F4+8Z+KA/PLlcdHR0UbcbFbwonzfeKp8TcTV1ftLPbs
fn8U+AzDWQAtvf0O1D3SPSdWpr7PRlAvFK9sDhgD/58y5QP4/trEJI50SNoczJRH
UiuY75ilDvKxB8LF50uoLC5zKmErhZiDVS1/mB3kNefLNXuobZFFU1fBA2X4NOad
+7LX0l7lGZ4GU1MCoQvvrRc6WuC/wN/yXzQx6vF6xftpBo7TsmQP13fapXolOi5M
Vq1La5TzcQoUrUJVikSmgNA0TGpImGdo+NrHUN7lAx/z/1UCAwEAAaN7MHkwDgYD
VR0PAQH/BAQDAgEGMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFLirN8iwJ/d+
2lwlJJaJFLlwWOYjMB8GA1UdIwQYMBaAFLirN8iwJ/d+2lwlJJaJFLlwWOYjMBYG
A1UdEQQPMA2CC2V4YW1wbGUuY29tMA0GCSqGSIb3DQEBCwUAA4IBAQCP07rxJ21f
7sTAC0GeUErgszwXDuvvD+82RpkY/QKcqRe2cK3Ohr0cYDBhtJrOO24gacuq60Lk
bAVr/FADhu2L6gSY3yXCi1WtkKVaKcA8E/UUvscSwaTx0Kks+iI3LUWaOuOhgtqo
mXUCItHTEvcphGzeDxIYLY3Y2l60hL+fSjQDftVX9qGg6U+o4oQQ47m8G1HW9bV6
pIO6TuEXlHMK/sF56Cp0OVCwiHTao736InoPV3fCL8dyW8GnxUzS14ngDlGq9063
FKGVRrz4ZVHGuQOASF0NTMc3ymr+Z3kHELoGdr/47Xdnkn2wp4FV9RyWoqZc6Stl
OS4IgCFIktG3
-----END CERTIFICATE-----
```

Настраиваем URL-адреса CA и CRL.

```bash
vagrant@vagrant:~$ vault write pki/config/urls issuing_certificates="$VAULT_ADDR/v1/pki/ca" crl_distribution_points="$VAULT_ADDR/v1/pki/crl"
Success! Data written to: pki/config/urls
```

Шаг 2: Создаем промежуточный ЦС и генерируем промежуточный сертификат.

Теперь мы создаем промежуточный центр сертификации, используя корневой центр сертификации,из предыдущего шага.

Включаем secrets engine pki по пути pki_int.

```bash
vagrant@vagrant:~$ vault secrets enable -path=pki_int pki
Success! Enabled the pki secrets engine at: pki_int/
```

Настраиваем secrets engine pki_int на выдачу сертификатов с максимальным временем жизни (TTL) 43800 часов.

```bash
vagrant@vagrant:~$ vault secrets tune -max-lease-ttl=43800h pki_int
Success! Tuned the secrets engine at: pki_int/
```

Генерируем промежуточный сертификат и сохраняем как pki_intermediate.csr.

```bash
vagrant@vagrant:~$ vault write -format=json pki_int/intermediate/generate/internal common_name="example.com Intermediate Authority" | jq -r '.data.csr' > pki_intermediate.csr
```

Проверим что сгенерировалось:

```bash
vagrant@vagrant:~$ cat pki_intermediate.csr
-----BEGIN CERTIFICATE REQUEST-----
MIICcjCCAVoCAQAwLTErMCkGA1UEAxMiZXhhbXBsZS5jb20gSW50ZXJtZWRpYXRl
IEF1dGhvcml0eTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALgnDZQM
T5dAQjpchQS4L1j3LHwfb2vIbNHStaqNlrDiBJ90vshSmteomGAJRkkL7CbmkJLz
2mhDWGgCuywZwaBaF3I3h8gtiqM+5ORflAmEqCar4FpCEJKsd8TpqCmAerjBy520
XSxuhSJEuYOiJNPA+5lj0UHt0PqAI6EksAmmWf7c04xllhOtUI4PU0sH7snSKNM3
F4oBC6OM4u5eZkklLQcKTdQAY0XYU6ysiKlNcdHAr+BRQWenFTcPEpD2mTu7uPuS
wqTiFJIA9Ypi3I5EKYk+GXhRoJcFA53i87GcY6bnQl0fz2JCX4ouf60fM7mGirxv
TAuBL7Ecqa8Zr2ECAwEAAaAAMA0GCSqGSIb3DQEBCwUAA4IBAQByh9Y9rA4Rws2F
i6YOIVTTRzkgWahllz2L4gO4hSq2zXhsuS2RUQnZFZCYarbH9yobdIyZ7g6P5H+O
sVQvnzE7yYQoDg2Xq+OiXr4Mb/avmzvUP44oF6AFfVQHX3YoA/kCA7UND2dxvcC9
71RdT76zB/v0xjgOIY7D6oHeQX/f3nHZ9EK445bPUQZEA8gW9oxnb/FnP7pZQ7no
5dXAAfgc/AJUozvICZ61BnKi+PkGFgaijCvEFuMka+cR30cxt2eF7L7sIvw0T1ZR
sMZxpWZswszO+QzvaYyg6Z8HjldJRFO7WWvG32BJPe8KtaVOGkWSiatKLImrgdD/
B6AFWNZc
-----END CERTIFICATE REQUEST-----
```

![2](img/img002.PNG)

Подписываем промежуточный сертификат закрытым ключом корневого центра сертификации и сохраните созданный сертификат как intermediate.cert.pem.

```bash
vagrant@vagrant:~$ vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.csr format=pem_bundle ttl="43800h" | jq -r '.data.certificate' > intermediate.cert.pem
```

Проверим что сгенерировалось:

```bash
vagrant@vagrant:~$ cat intermediate.cert.pem
-----BEGIN CERTIFICATE-----
MIIDpjCCAo6gAwIBAgIUAU1x27wq6jBs8Vw4kaVTphXnfucwDQYJKoZIhvcNAQEL
BQAwFjEUMBIGA1UEAxMLZXhhbXBsZS5jb20wHhcNMjIwMzI3MjE1OTU4WhcNMjcw
MzI2MjIwMDI4WjAtMSswKQYDVQQDEyJleGFtcGxlLmNvbSBJbnRlcm1lZGlhdGUg
QXV0aG9yaXR5MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuCcNlAxP
l0BCOlyFBLgvWPcsfB9va8hs0dK1qo2WsOIEn3S+yFKa16iYYAlGSQvsJuaQkvPa
aENYaAK7LBnBoFoXcjeHyC2Koz7k5F+UCYSoJqvgWkIQkqx3xOmoKYB6uMHLnbRd
LG6FIkS5g6Ik08D7mWPRQe3Q+oAjoSSwCaZZ/tzTjGWWE61Qjg9TSwfuydIo0zcX
igELo4zi7l5mSSUtBwpN1ABjRdhTrKyIqU1x0cCv4FFBZ6cVNw8SkPaZO7u4+5LC
pOIUkgD1imLcjkQpiT4ZeFGglwUDneLzsZxjpudCXR/PYkJfii5/rR8zuYaKvG9M
C4EvsRyprxmvYQIDAQABo4HUMIHRMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMBAf8E
BTADAQH/MB0GA1UdDgQWBBRqgJFaHCCh4j8S1aCmETtdhkByiTAfBgNVHSMEGDAW
gBS4qzfIsCf3ftpcJSSWiRS5cFjmIzA7BggrBgEFBQcBAQQvMC0wKwYIKwYBBQUH
MAKGH2h0dHA6Ly8xMjcuMC4wLjE6ODIwMC92MS9wa2kvY2EwMQYDVR0fBCowKDAm
oCSgIoYgaHR0cDovLzEyNy4wLjAuMTo4MjAwL3YxL3BraS9jcmwwDQYJKoZIhvcN
AQELBQADggEBACEPJyavyNypJHvsKa5RUGGyUmxvkb/yGEplOnxSvpi6W+r2pQ80
bUY+gptOPcsa5iQySv6Hzu85zsjiEz2YjEzdy4/tDoeGIEtLSPlpPfVxvArdTC6C
FSeqWPspHNJKFZdE59qPiucrqsSw119f62VoMjP6Do3ZGrxCoE+jqwouyT0hcxEp
+Ry/LTlsaO6FBvtqrghoOnjhB9588SUCAEwmT/vOBneDstSqTA9zK1meBbs0U/QM
oJ/tB8Bnk8ATPKxXRBuIobaUx1FOIu9hFHzyKu87EiX2cDMRzhCYdERNLnEYnXF6
5I+fkXInRDN2YkJyHdtYonjvPWsavoQuQrE=
-----END CERTIFICATE-----
```

Как только CSR будет подписан и корневой центр сертификации вернет сертификат, его можно будет импортировать обратно в Vault.

```bash
vagrant@vagrant:~$ vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem
Success! Data written to: pki_int/intermediate/set-signed
```

Шаг 3. Создание роли.

Роль - это логическое имя, которое соответствует политике, используемой для создания этих учетных данных. Это позволяет параметрам конфигурации управлять общими именами сертификатов, альтернативными именами, использованием ключей, для которых они действительны, и многим другим.

Вот несколько примечательных параметров:

`allowed_domains`	Задает домены роли (используется с параметрами allow_bare_domains и allow-subdomains)

`allow_bare_domains`	Указывает, могут ли клиенты запрашивать сертификаты, соответствующие значению самих фактических доменов

`allow_subdomains`	Указывает, могут ли клиенты запрашивать сертификаты с CN, которые являются поддоменами CN, разрешенными другими параметрами роли (ПРИМЕЧАНИЕ: сюда входят wildcard поддомены).

`allow_glob_domains`	Позволяет именам, указанным в allowed_domains, содержать глобальные шаблоны (например, ftp*.example.com )

Создадим роль с именем example-dot-com, которая разрешает поддомены.

```bash
vagrant@vagrant:~$ vault write pki_int/roles/example-dot-com allowed_domains="example.com" allow_bare_domains=true allow_subdomains=true max_ttl="720h"
Success! Data written to: pki_int/roles/example-dot-com
```

Шаг 4. Запрос сертификатов

Запросим новый сертификат для домена example.com, основанный на роли example-dot-com.

```bash
vagrant@vagrant:~$ vault write -format=json pki_int/issue/example-dot-com common_name="example.com" ttl="720h" > example.com.crt
```

Проверим что всё получилось:

```bash
vagrant@vagrant:~$ cat example.com.crt
{
  "request_id": "753238b2-5209-8932-65c8-5e053860a99f",
  "lease_id": "",
  "lease_duration": 0,
  "renewable": false,
  "data": {
    "ca_chain": [
      "-----BEGIN CERTIFICATE-----\nMIIDpjCCAo6gAwIBAgIUAU1x27wq6jBs8Vw4kaVTphXnfucwDQYJKoZIhvcNAQEL\nBQAwFjEUMBIGA1UEAxMLZXhhbXBsZS5jb20wHhcNMjIwMzI3MjE1OTU4WhcNMjcw\nMzI2MjIwMDI4WjAtMSswKQYDVQQDEyJleGFtcGxlLmNvbSBJbnRlcm1lZGlhdGUg\nQXV0aG9yaXR5MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuCcNlAxP\nl0BCOlyFBLgvWPcsfB9va8hs0dK1qo2WsOIEn3S+yFKa16iYYAlGSQvsJuaQkvPa\naENYaAK7LBnBoFoXcjeHyC2Koz7k5F+UCYSoJqvgWkIQkqx3xOmoKYB6uMHLnbRd\nLG6FIkS5g6Ik08D7mWPRQe3Q+oAjoSSwCaZZ/tzTjGWWE61Qjg9TSwfuydIo0zcX\nigELo4zi7l5mSSUtBwpN1ABjRdhTrKyIqU1x0cCv4FFBZ6cVNw8SkPaZO7u4+5LC\npOIUkgD1imLcjkQpiT4ZeFGglwUDneLzsZxjpudCXR/PYkJfii5/rR8zuYaKvG9M\nC4EvsRyprxmvYQIDAQABo4HUMIHRMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMBAf8E\nBTADAQH/MB0GA1UdDgQWBBRqgJFaHCCh4j8S1aCmETtdhkByiTAfBgNVHSMEGDAW\ngBS4qzfIsCf3ftpcJSSWiRS5cFjmIzA7BggrBgEFBQcBAQQvMC0wKwYIKwYBBQUH\nMAKGH2h0dHA6Ly8xMjcuMC4wLjE6ODIwMC92MS9wa2kvY2EwMQYDVR0fBCowKDAm\noCSgIoYgaHR0cDovLzEyNy4wLjAuMTo4MjAwL3YxL3BraS9jcmwwDQYJKoZIhvcN\nAQELBQADggEBACEPJyavyNypJHvsKa5RUGGyUmxvkb/yGEplOnxSvpi6W+r2pQ80\nbUY+gptOPcsa5iQySv6Hzu85zsjiEz2YjEzdy4/tDoeGIEtLSPlpPfVxvArdTC6C\nFSeqWPspHNJKFZdE59qPiucrqsSw119f62VoMjP6Do3ZGrxCoE+jqwouyT0hcxEp\n+Ry/LTlsaO6FBvtqrghoOnjhB9588SUCAEwmT/vOBneDstSqTA9zK1meBbs0U/QM\noJ/tB8Bnk8ATPKxXRBuIobaUx1FOIu9hFHzyKu87EiX2cDMRzhCYdERNLnEYnXF6\n5I+fkXInRDN2YkJyHdtYonjvPWsavoQuQrE=\n-----END CERTIFICATE-----"
    ],
    "certificate": "-----BEGIN CERTIFICATE-----\nMIIDXDCCAkSgAwIBAgIUG7P+RyClZS3qkFgFX/eVy5LKK5EwDQYJKoZIhvcNAQEL\nBQAwLTErMCkGA1UEAxMiZXhhbXBsZS5jb20gSW50ZXJtZWRpYXRlIEF1dGhvcml0\neTAeFw0yMjAzMjcyMjI4MThaFw0yMjA0MjYyMjI4NDdaMBYxFDASBgNVBAMTC2V4\nYW1wbGUuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7jvT9coV\nwvRHZD8dRkGW33+tSLRiuA1RYC3i7ciZLM+VKCq5aat2xTL3ypiJt79/hY/AhuPX\ntcve0d0fjh+RG6CE5Dh43kAUGTc/GtC8f7tJpKxdgv3913ZyusPpJ08zIob7Ny5m\nB8wOcZA/vYJDhWfb3ZNUzT5ONIznwnjUm5bhiiuaPkbBUIgrr9TH3290cUXGd/1T\nbey/fLvLFTcgwwCl80nT+4hkaWzLfYmv4BAO2qtVrcfvrsBt/j3j2p+hQcrUktPu\nH1Md8/n9TNaX7Rb8EpxJv2gq9xDdDFKLFdVc4bJ4VoUSUwe6Ii1WYqgc3xsLN7Bd\n9rdKEcGeEz35uQIDAQABo4GKMIGHMA4GA1UdDwEB/wQEAwIDqDAdBgNVHSUEFjAU\nBggrBgEFBQcDAQYIKwYBBQUHAwIwHQYDVR0OBBYEFP+9yWXV7/8gKmuZPGKcmpZI\n/iNIMB8GA1UdIwQYMBaAFGqAkVocIKHiPxLVoKYRO12GQHKJMBYGA1UdEQQPMA2C\nC2V4YW1wbGUuY29tMA0GCSqGSIb3DQEBCwUAA4IBAQCkE54cxI0OH+ZQop4t/QgS\nt28baRT/klw7cVt2+ulZv3BACnYokJnOBFO2w2Chu9cugqBLHr80jwR6JVpmB3Zl\nNkcHV7Ej6zrMS+ClyoRA1gWZii8tIwoJEIfFxl2xkpXEsBQTU/K2FLHzOzj1UcgG\n9qHYXkjo1gqby2yzQrKO2JMisHwUUOGDS/N6CQWgFp01tgZHenbaZ7IyJNWbCYTT\nRai5AxqQU6gC2jkwuPx/olrnkFaTRKbbh45B1wIJp3JblUmGwy8s+F7Ok39JZCSy\nH2yGNDUg83AWEoiVr0OKkkYxsobNhqiEBs0Q4C7LBqWQCG7zA1DBKQ+95BtWzqDT\n-----END CERTIFICATE-----",
    "expiration": 1651012127,
    "issuing_ca": "-----BEGIN CERTIFICATE-----\nMIIDpjCCAo6gAwIBAgIUAU1x27wq6jBs8Vw4kaVTphXnfucwDQYJKoZIhvcNAQEL\nBQAwFjEUMBIGA1UEAxMLZXhhbXBsZS5jb20wHhcNMjIwMzI3MjE1OTU4WhcNMjcw\nMzI2MjIwMDI4WjAtMSswKQYDVQQDEyJleGFtcGxlLmNvbSBJbnRlcm1lZGlhdGUg\nQXV0aG9yaXR5MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuCcNlAxP\nl0BCOlyFBLgvWPcsfB9va8hs0dK1qo2WsOIEn3S+yFKa16iYYAlGSQvsJuaQkvPa\naENYaAK7LBnBoFoXcjeHyC2Koz7k5F+UCYSoJqvgWkIQkqx3xOmoKYB6uMHLnbRd\nLG6FIkS5g6Ik08D7mWPRQe3Q+oAjoSSwCaZZ/tzTjGWWE61Qjg9TSwfuydIo0zcX\nigELo4zi7l5mSSUtBwpN1ABjRdhTrKyIqU1x0cCv4FFBZ6cVNw8SkPaZO7u4+5LC\npOIUkgD1imLcjkQpiT4ZeFGglwUDneLzsZxjpudCXR/PYkJfii5/rR8zuYaKvG9M\nC4EvsRyprxmvYQIDAQABo4HUMIHRMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMBAf8E\nBTADAQH/MB0GA1UdDgQWBBRqgJFaHCCh4j8S1aCmETtdhkByiTAfBgNVHSMEGDAW\ngBS4qzfIsCf3ftpcJSSWiRS5cFjmIzA7BggrBgEFBQcBAQQvMC0wKwYIKwYBBQUH\nMAKGH2h0dHA6Ly8xMjcuMC4wLjE6ODIwMC92MS9wa2kvY2EwMQYDVR0fBCowKDAm\noCSgIoYgaHR0cDovLzEyNy4wLjAuMTo4MjAwL3YxL3BraS9jcmwwDQYJKoZIhvcN\nAQELBQADggEBACEPJyavyNypJHvsKa5RUGGyUmxvkb/yGEplOnxSvpi6W+r2pQ80\nbUY+gptOPcsa5iQySv6Hzu85zsjiEz2YjEzdy4/tDoeGIEtLSPlpPfVxvArdTC6C\nFSeqWPspHNJKFZdE59qPiucrqsSw119f62VoMjP6Do3ZGrxCoE+jqwouyT0hcxEp\n+Ry/LTlsaO6FBvtqrghoOnjhB9588SUCAEwmT/vOBneDstSqTA9zK1meBbs0U/QM\noJ/tB8Bnk8ATPKxXRBuIobaUx1FOIu9hFHzyKu87EiX2cDMRzhCYdERNLnEYnXF6\n5I+fkXInRDN2YkJyHdtYonjvPWsavoQuQrE=\n-----END CERTIFICATE-----",
    "private_key": "-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEA7jvT9coVwvRHZD8dRkGW33+tSLRiuA1RYC3i7ciZLM+VKCq5\naat2xTL3ypiJt79/hY/AhuPXtcve0d0fjh+RG6CE5Dh43kAUGTc/GtC8f7tJpKxd\ngv3913ZyusPpJ08zIob7Ny5mB8wOcZA/vYJDhWfb3ZNUzT5ONIznwnjUm5bhiiua\nPkbBUIgrr9TH3290cUXGd/1Tbey/fLvLFTcgwwCl80nT+4hkaWzLfYmv4BAO2qtV\nrcfvrsBt/j3j2p+hQcrUktPuH1Md8/n9TNaX7Rb8EpxJv2gq9xDdDFKLFdVc4bJ4\nVoUSUwe6Ii1WYqgc3xsLN7Bd9rdKEcGeEz35uQIDAQABAoIBAQDebaOf99dLl5HU\nag0mHHUGJYofuLP3DhAtUYpv4nwJV6L2xrUokPuqcMTkNnlWwwgIJshl6PLs/PUE\nUoV0x8pO1hddkdBgCcn6JRfZLIziYXYHtxr0A7ruYdwKvoHAvvSKRybkRYDjxMSz\niS/J+4aZVvf0L+vcWVDhRbHZY8F1paOCNISVKWeFEyry8viUVOZY5zKjlibpeuyV\nMmeSzAGkQQq5x5wEQapXwI0cBz/D34sEG6t7lRAzHq30Rc2feFFNcQ0eugvLiw4m\nzLfz33RP7rdM8H1+aZEZEoXCdoYAwLsR0R07JHlPbyYBdVpVDJfQKVUEUI63TzRe\nk6BBArTFAoGBAO/GzpPajLdK7MfvAomkB4RiBVMkMP0XuGt7prIogfaDPD7/aJD1\nc4nQstoT9WWPkQDNKINV7adtz6d/XB40mscVJecXdI3GbNAURR7MjGf36ZMpid43\n66KtSHbeJtZXitq33CjCytWpxOTsB0O+LJHGtzyLsNpnaZ7Zf94oa4lXAoGBAP5a\nS+oN5rGYngEhBM018skUkBcbC9+4aROi+ARbP57ZbwykjfFv1NtLJKZ9zmUrYpSo\nhleHI6/sGT2JS9sbGggImHMIWQko0gw27QZLaNltd/v825pFRidoC6ddBgEVTUIH\nPry9Fc4Tkpgo2eqvmWHqYnjRhRN6OdflFF1u4NtvAoGBAKBFRQOzS+egn1CsxAd4\nqsWkN2bxhAVIe67sgeoIBYbfBcAePKjYSBhQdZwrRxZRtlzQxUm0gBwv3GNbUBmo\nk+SKkEE9flzdyxHy2pjRpPBB19DULSFqQ4kDRrKdn1waO+giiXh9a9MRnVhfJCP1\n1BjEuOoxfU8fXIwfWccHQYoVAoGBAJzmQIv51UPaXCVgI+EelUya5aOLKJDx5cea\nMRom26D2ib0nyPOVQ52exdX6JxZbY+1F49EcaNQ9dPhzuBpJpo4sFzZmgN3Yk3G7\ndAz8+YmeMHR9701DzFnEoeO0y15hsI25gGbW0RuVEUnRcVOGzLwM5H+Y51kzfXkD\nM8PLAOP7AoGADBlJSIPJ02DpjZJOecnL3vrvVq9PqNd4Ub1sS4MEW3CBcubQTrfu\nOEsTH1yAi2HkgZZb6IZgryOHytzggyZzd9szeRdhBd2SA7qsIX2lic8jMKIiOb6K\n7zT06ezUyKQPh6Idgu/T+j1w+soDzT2qa2hRBUbZcBesUcEAFRdGjwA=\n-----END RSA PRIVATE KEY-----",
    "private_key_type": "rsa",
    "serial_number": "1b:b3:fe:47:20:a5:65:2d:ea:90:58:05:5f:f7:95:cb:92:ca:2b:91"
  },
  "warnings": null
}
```

Далее нам нужно поделить этот файл с сертификатами, на открытую и закрытую часть.

Открытая часть будет содержать ca_chain и certificate и поместим в файл .pem, а закрытая - приватный ключ private_key и поместим в файл .key, это нам понадобится для сервера nginx.

Для разделения так же воспользуемся утилитой jq:

Сначала private_key:

```bash
vagrant@vagrant:~$ cat example.com.crt | jq -r .data.private_key > example.com.crt.key
```

Проверим:

```bash
vagrant@vagrant:~$ cat example.com.crt.key
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA7jvT9coVwvRHZD8dRkGW33+tSLRiuA1RYC3i7ciZLM+VKCq5
aat2xTL3ypiJt79/hY/AhuPXtcve0d0fjh+RG6CE5Dh43kAUGTc/GtC8f7tJpKxd
gv3913ZyusPpJ08zIob7Ny5mB8wOcZA/vYJDhWfb3ZNUzT5ONIznwnjUm5bhiiua
PkbBUIgrr9TH3290cUXGd/1Tbey/fLvLFTcgwwCl80nT+4hkaWzLfYmv4BAO2qtV
rcfvrsBt/j3j2p+hQcrUktPuH1Md8/n9TNaX7Rb8EpxJv2gq9xDdDFKLFdVc4bJ4
VoUSUwe6Ii1WYqgc3xsLN7Bd9rdKEcGeEz35uQIDAQABAoIBAQDebaOf99dLl5HU
ag0mHHUGJYofuLP3DhAtUYpv4nwJV6L2xrUokPuqcMTkNnlWwwgIJshl6PLs/PUE
UoV0x8pO1hddkdBgCcn6JRfZLIziYXYHtxr0A7ruYdwKvoHAvvSKRybkRYDjxMSz
iS/J+4aZVvf0L+vcWVDhRbHZY8F1paOCNISVKWeFEyry8viUVOZY5zKjlibpeuyV
MmeSzAGkQQq5x5wEQapXwI0cBz/D34sEG6t7lRAzHq30Rc2feFFNcQ0eugvLiw4m
zLfz33RP7rdM8H1+aZEZEoXCdoYAwLsR0R07JHlPbyYBdVpVDJfQKVUEUI63TzRe
k6BBArTFAoGBAO/GzpPajLdK7MfvAomkB4RiBVMkMP0XuGt7prIogfaDPD7/aJD1
c4nQstoT9WWPkQDNKINV7adtz6d/XB40mscVJecXdI3GbNAURR7MjGf36ZMpid43
66KtSHbeJtZXitq33CjCytWpxOTsB0O+LJHGtzyLsNpnaZ7Zf94oa4lXAoGBAP5a
S+oN5rGYngEhBM018skUkBcbC9+4aROi+ARbP57ZbwykjfFv1NtLJKZ9zmUrYpSo
hleHI6/sGT2JS9sbGggImHMIWQko0gw27QZLaNltd/v825pFRidoC6ddBgEVTUIH
Pry9Fc4Tkpgo2eqvmWHqYnjRhRN6OdflFF1u4NtvAoGBAKBFRQOzS+egn1CsxAd4
qsWkN2bxhAVIe67sgeoIBYbfBcAePKjYSBhQdZwrRxZRtlzQxUm0gBwv3GNbUBmo
k+SKkEE9flzdyxHy2pjRpPBB19DULSFqQ4kDRrKdn1waO+giiXh9a9MRnVhfJCP1
1BjEuOoxfU8fXIwfWccHQYoVAoGBAJzmQIv51UPaXCVgI+EelUya5aOLKJDx5cea
MRom26D2ib0nyPOVQ52exdX6JxZbY+1F49EcaNQ9dPhzuBpJpo4sFzZmgN3Yk3G7
dAz8+YmeMHR9701DzFnEoeO0y15hsI25gGbW0RuVEUnRcVOGzLwM5H+Y51kzfXkD
M8PLAOP7AoGADBlJSIPJ02DpjZJOecnL3vrvVq9PqNd4Ub1sS4MEW3CBcubQTrfu
OEsTH1yAi2HkgZZb6IZgryOHytzggyZzd9szeRdhBd2SA7qsIX2lic8jMKIiOb6K
7zT06ezUyKQPh6Idgu/T+j1w+soDzT2qa2hRBUbZcBesUcEAFRdGjwA=
-----END RSA PRIVATE KEY-----
```

Затем ca_chain и certificate:

```bash
vagrant@vagrant:~$ cat example.com.crt | jq -r .data.certificate > example.com.crt.pem
vagrant@vagrant:~$ cat example.com.crt | jq -r .data.ca_chain[] >> example.com.crt.pem
```

Проверим:

```bash
vagrant@vagrant:~$ cat example.com.crt.pem
-----BEGIN CERTIFICATE-----
MIIDXDCCAkSgAwIBAgIUG7P+RyClZS3qkFgFX/eVy5LKK5EwDQYJKoZIhvcNAQEL
BQAwLTErMCkGA1UEAxMiZXhhbXBsZS5jb20gSW50ZXJtZWRpYXRlIEF1dGhvcml0
eTAeFw0yMjAzMjcyMjI4MThaFw0yMjA0MjYyMjI4NDdaMBYxFDASBgNVBAMTC2V4
YW1wbGUuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7jvT9coV
wvRHZD8dRkGW33+tSLRiuA1RYC3i7ciZLM+VKCq5aat2xTL3ypiJt79/hY/AhuPX
tcve0d0fjh+RG6CE5Dh43kAUGTc/GtC8f7tJpKxdgv3913ZyusPpJ08zIob7Ny5m
B8wOcZA/vYJDhWfb3ZNUzT5ONIznwnjUm5bhiiuaPkbBUIgrr9TH3290cUXGd/1T
bey/fLvLFTcgwwCl80nT+4hkaWzLfYmv4BAO2qtVrcfvrsBt/j3j2p+hQcrUktPu
H1Md8/n9TNaX7Rb8EpxJv2gq9xDdDFKLFdVc4bJ4VoUSUwe6Ii1WYqgc3xsLN7Bd
9rdKEcGeEz35uQIDAQABo4GKMIGHMA4GA1UdDwEB/wQEAwIDqDAdBgNVHSUEFjAU
BggrBgEFBQcDAQYIKwYBBQUHAwIwHQYDVR0OBBYEFP+9yWXV7/8gKmuZPGKcmpZI
/iNIMB8GA1UdIwQYMBaAFGqAkVocIKHiPxLVoKYRO12GQHKJMBYGA1UdEQQPMA2C
C2V4YW1wbGUuY29tMA0GCSqGSIb3DQEBCwUAA4IBAQCkE54cxI0OH+ZQop4t/QgS
t28baRT/klw7cVt2+ulZv3BACnYokJnOBFO2w2Chu9cugqBLHr80jwR6JVpmB3Zl
NkcHV7Ej6zrMS+ClyoRA1gWZii8tIwoJEIfFxl2xkpXEsBQTU/K2FLHzOzj1UcgG
9qHYXkjo1gqby2yzQrKO2JMisHwUUOGDS/N6CQWgFp01tgZHenbaZ7IyJNWbCYTT
Rai5AxqQU6gC2jkwuPx/olrnkFaTRKbbh45B1wIJp3JblUmGwy8s+F7Ok39JZCSy
H2yGNDUg83AWEoiVr0OKkkYxsobNhqiEBs0Q4C7LBqWQCG7zA1DBKQ+95BtWzqDT
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIDpjCCAo6gAwIBAgIUAU1x27wq6jBs8Vw4kaVTphXnfucwDQYJKoZIhvcNAQEL
BQAwFjEUMBIGA1UEAxMLZXhhbXBsZS5jb20wHhcNMjIwMzI3MjE1OTU4WhcNMjcw
MzI2MjIwMDI4WjAtMSswKQYDVQQDEyJleGFtcGxlLmNvbSBJbnRlcm1lZGlhdGUg
QXV0aG9yaXR5MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuCcNlAxP
l0BCOlyFBLgvWPcsfB9va8hs0dK1qo2WsOIEn3S+yFKa16iYYAlGSQvsJuaQkvPa
aENYaAK7LBnBoFoXcjeHyC2Koz7k5F+UCYSoJqvgWkIQkqx3xOmoKYB6uMHLnbRd
LG6FIkS5g6Ik08D7mWPRQe3Q+oAjoSSwCaZZ/tzTjGWWE61Qjg9TSwfuydIo0zcX
igELo4zi7l5mSSUtBwpN1ABjRdhTrKyIqU1x0cCv4FFBZ6cVNw8SkPaZO7u4+5LC
pOIUkgD1imLcjkQpiT4ZeFGglwUDneLzsZxjpudCXR/PYkJfii5/rR8zuYaKvG9M
C4EvsRyprxmvYQIDAQABo4HUMIHRMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMBAf8E
BTADAQH/MB0GA1UdDgQWBBRqgJFaHCCh4j8S1aCmETtdhkByiTAfBgNVHSMEGDAW
gBS4qzfIsCf3ftpcJSSWiRS5cFjmIzA7BggrBgEFBQcBAQQvMC0wKwYIKwYBBQUH
MAKGH2h0dHA6Ly8xMjcuMC4wLjE6ODIwMC92MS9wa2kvY2EwMQYDVR0fBCowKDAm
oCSgIoYgaHR0cDovLzEyNy4wLjAuMTo4MjAwL3YxL3BraS9jcmwwDQYJKoZIhvcN
AQELBQADggEBACEPJyavyNypJHvsKa5RUGGyUmxvkb/yGEplOnxSvpi6W+r2pQ80
bUY+gptOPcsa5iQySv6Hzu85zsjiEz2YjEzdy4/tDoeGIEtLSPlpPfVxvArdTC6C
FSeqWPspHNJKFZdE59qPiucrqsSw119f62VoMjP6Do3ZGrxCoE+jqwouyT0hcxEp
+Ry/LTlsaO6FBvtqrghoOnjhB9588SUCAEwmT/vOBneDstSqTA9zK1meBbs0U/QM
oJ/tB8Bnk8ATPKxXRBuIobaUx1FOIu9hFHzyKu87EiX2cDMRzhCYdERNLnEYnXF6
5I+fkXInRDN2YkJyHdtYonjvPWsavoQuQrE=
-----END CERTIFICATE-----
```

---

5. Установите корневой сертификат созданного центра сертификации в доверенные в хостовой системе.

---

Подключаемся через WinSCP, скидываем сертификат на хост и устанавливаем в доверенные корневые ЦС.

![3](img/img003.PNG)

![4](img/img004.PNG)

---

6. Установите nginx.

---

```bash
vagrant@vagrant:~$ sudo apt install nginx
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following package was automatically installed and is no longer required:
  libfwupdplugin1
Use 'sudo apt autoremove' to remove it.
The following additional packages will be installed:
  fontconfig-config fonts-dejavu-core libfontconfig1 libgd3 libjbig0 libjpeg-turbo8 libjpeg8
  libnginx-mod-http-image-filter libnginx-mod-http-xslt-filter libnginx-mod-mail libnginx-mod-stream
  libtiff5 libwebp6 libx11-6 libx11-data libxau6 libxcb1 libxdmcp6 libxpm4 nginx-common nginx-core
Suggested packages:
  libgd-tools fcgiwrap nginx-doc ssl-cert
The following NEW packages will be installed:
  fontconfig-config fonts-dejavu-core libfontconfig1 libgd3 libjbig0 libjpeg-turbo8 libjpeg8
  libnginx-mod-http-image-filter libnginx-mod-http-xslt-filter libnginx-mod-mail libnginx-mod-stream
  libtiff5 libwebp6 libx11-6 libx11-data libxau6 libxcb1 libxdmcp6 libxpm4 nginx nginx-common nginx-core
0 upgraded, 22 newly installed, 0 to remove and 0 not upgraded.
Need to get 3,183 kB of archives.
After this operation, 11.1 MB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://us.archive.ubuntu.com/ubuntu focal/main amd64 libxau6 amd64 1:1.0.9-0ubuntu1 [7,488 B]
Get:2 http://us.archive.ubuntu.com/ubuntu focal/main amd64 libxdmcp6 amd64 1:1.1.3-0ubuntu1 [10.6 kB]
Get:3 http://us.archive.ubuntu.com/ubuntu focal/main amd64 libxcb1 amd64 1.14-2 [44.7 kB]
Get:4 http://us.archive.ubuntu.com/ubuntu focal-updates/main amd64 libx11-data all 2:1.6.9-2ubuntu1.2 [113 kB]
Get:5 http://us.archive.ubuntu.com/ubuntu focal-updates/main amd64 libx11-6 amd64 2:1.6.9-2ubuntu1.2 [575 kB]
Setting up libxau6:amd64 (1:1.0.9-0ubuntu1) ...
Setting up libxdmcp6:amd64 (1:1.1.3-0ubuntu1) ...
Setting up libxcb1:amd64 (1.14-2) ...
Setting up nginx-common (1.18.0-0ubuntu1.2) ...
Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /lib/systemd/system/nginx.service.
Setting up libjbig0:amd64 (2.1-3.1build1) ...
Setting up libnginx-mod-http-xslt-filter (1.18.0-0ubuntu1.2) ...
Setting up libx11-data (2:1.6.9-2ubuntu1.2) ...
Setting up libwebp6:amd64 (0.6.1-2ubuntu0.20.04.1) ...
Setting up fonts-dejavu-core (2.37-1) ...
Setting up libjpeg-turbo8:amd64 (2.0.3-0ubuntu1.20.04.1) ...
Setting up libx11-6:amd64 (2:1.6.9-2ubuntu1.2) ...
Setting up libjpeg8:amd64 (8c-2ubuntu8) ...
Setting up libnginx-mod-mail (1.18.0-0ubuntu1.2) ...
Setting up libxpm4:amd64 (1:3.5.12-1) ...
Setting up fontconfig-config (2.13.1-2ubuntu3) ...
Setting up libnginx-mod-stream (1.18.0-0ubuntu1.2) ...
Setting up libtiff5:amd64 (4.1.0+git191117-2ubuntu0.20.04.2) ...
Setting up libfontconfig1:amd64 (2.13.1-2ubuntu3) ...
Setting up libgd3:amd64 (2.2.5-5.2ubuntu2.1) ...
Setting up libnginx-mod-http-image-filter (1.18.0-0ubuntu1.2) ...
Setting up nginx-core (1.18.0-0ubuntu1.2) ...
Setting up nginx (1.18.0-0ubuntu1.2) ...
Processing triggers for ufw (0.36-6ubuntu1) ...
Processing triggers for systemd (245.4-4ubuntu3.15) ...
Processing triggers for man-db (2.9.1-1) ...
Processing triggers for libc-bin (2.31-0ubuntu9.7) ...
```

Проверим что запустился:

```bash
vagrant@vagrant:~$ sudo systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2022-03-27 22:43:03 UTC; 1min 1s ago
       Docs: man:nginx(8)
   Main PID: 2595 (nginx)
      Tasks: 3 (limit: 4653)
     Memory: 6.7M
     CGroup: /system.slice/nginx.service
             ├─2595 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
             ├─2596 nginx: worker process
             └─2597 nginx: worker process

Mar 27 22:43:03 vagrant systemd[1]: Starting A high performance web server and a reverse proxy server...
Mar 27 22:43:03 vagrant systemd[1]: Started A high performance web server and a reverse proxy server.
```

---


7. По инструкции ([ссылка](https://nginx.org/en/docs/http/configuring_https_servers.html)) настройте nginx на https, используя ранее подготовленный сертификат:
- можно использовать стандартную стартовую страницу nginx для демонстрации работы сервера;
- можно использовать и другой html файл, сделанный вами;

---

Используем немного измененную стандартную страницу страницу:

```bash
vagrant@vagrant:~$ sudo mkdir /var/www/html/example.com
vagrant@vagrant:~$ sudo cp /var/www/html/index.nginx-debian.html /var/www/html/example.com/index.nginx-debian.html
vagrant@vagrant:~$ sudo chown www-data:www-data -R /var/www/html/example.com
vagrant@vagrant:~$ cat /var/www/html/example.comindex.nginx-debian.html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<h2>Нетология. Федоров Николай. Vault. Курсовая работа. 28.03.2022</h2>
<a href="https://github.com/kofe88/devops-netology/tree/main/pcs-devsys-diplom">https://github.com/kofe88/devops-netology/tree/main/pcs-devsys-diplom</a><br/>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

Сконфигурируем виртуальный хост nginx:

```bash
vagrant@vagrant:~$ sudo vi /etc/nginx/sites-available/example.com.conf

server {
        listen 80;
        listen [::]:80;
        server_name XXXX fail_timeout=0;
        return 301 https://XXXXX$request_uri;
}

server {
        listen [::]:443;
        listen              443 ssl;
        server_name         example.com;
        ssl_certificate     /home/vagrant/example.com.crt.pem;
        ssl_certificate_key /home/vagrant/example.com.crt.key;
        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers         HIGH:!aNULL:!MD5;
        root /var/www/html/example.com;
        index index.nginx-debian.html;
}
```

Включим виртуальный хост и перезапустим nginx:

```bash
vagrant@vagrant:~$ sudo ln -s /etc/nginx/sites-available/example.com.conf /etc/nginx/sites-enabled/example.com.conf
vagrant@vagrant:~$ sudo systemctl reload nginx
```
---

8. Откройте в браузере на хосте https адрес страницы, которую обслуживает сервер nginx.

---

Добавляем example.com временно в DNS роутера, в моем случае Mikrotik, чтобы можно было зайти по имени и не прописывать в host файл:

![5](img/img005.PNG)

Переходим по адресу https://example.com:1443 и проверяем что всё работает

![6](img/img006.PNG)

![7](img/img007.PNG)

---

9. Создайте скрипт, который будет генерировать новый сертификат в vault:
- генерируем новый сертификат так, чтобы не переписывать конфиг nginx;
- перезапускаем nginx для применения нового сертификата.

---

Скрипт:

```bash
vagrant@vagrant:~$ vi generate_crt.sh

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
```

ugo+x - разрешить выполнение для всех

```bash
vagrant@vagrant:~$ chmod ugo+x generate_crt.sh
```
Результат выполнения

```bash
vagrant@vagrant:~$ sudo ./generate_crt.sh
WARNING! The following warnings were returned from Vault:

  * Tidy operation successfully started. Any information from the operation
  will be printed to Vault's server logs.

nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
vagrant@vagrant:~$ cat generate_crt.log
Mon 28 Mar 2022 12:06:20 AM UTC
Expired cert removed
New cert issued
Expiration date:  Wed 27 Apr 2022 12:06:20 AM UTC
Nginx config test passed
Nginx succsessfully reloaded
```

![8](img/img008.PNG)

Проверка что новый сертификат работает. Время в логе UTC, в хосте GMT+3:

![9](img/img009.PNG)

Как видим дата и время совпадают, всё работает.

---

10. Поместите скрипт в crontab, чтобы сертификат обновлялся какого-то числа каждого месяца в удобное для вас время.

---

Для проверки чтобы долго не ждать, поставим на 5 минут.

```bash
vagrant@vagrant:~$ sudo vi /etc/crontab
```

```bash
*/5 * * * * /home/vagrant/generate_crt.sh
```

Результат:

![10](img/img010.PNG)
---

## Результат

Результатом курсовой работы должны быть снимки экрана или текст:

- Процесс установки и настройки ufw
- Процесс установки и выпуска сертификата с помощью hashicorp vault
- Процесс установки и настройки сервера nginx
- Страница сервера nginx в браузере хоста не содержит предупреждений
- Скрипт генерации нового сертификата работает (сертификат сервера ngnix должен быть "зеленым")
- Crontab работает (выберите число и время так, чтобы показать что crontab запускается и делает что надо)

## Как сдавать курсовую работу

Курсовую работу выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в [Google Docs](https://docs.google.com/document/u/0/?tgif=d) и отправить в личном кабинете на проверку ссылку на ваш документ.
Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу.
Ссылка на инструкцию [Как предоставить доступ к файлам и папкам на Google Диске](https://support.google.com/docs/answer/2494822?hl=ru&co=GENIE.Platform%3DDesktop).
