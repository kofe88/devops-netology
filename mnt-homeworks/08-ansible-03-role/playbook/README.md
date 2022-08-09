# 08-ansible-03-role
08-ansible-03-role

## Описание

Данный плейбук разворачивает на хостах `kibana` и `elascticsearch` соответствующие сервисы и `Oracle jdk`

`Oracle jdk` необходимо поместить в папку `files` в формате `.tar.gz` предварительно скачав с официального сайта.

`Kibana` и `Elasticsearch` скачиваются напрямую с сайтов разработчиков ( нужен VPN для РФ)

## Параметры

### vars

В каталогах расположены переменные для соответствующих хостов.


#### kibana

Для хоста `kibana`. 

`vars.yml`

```yaml
---
kibana_version: "8.3.3"
kibana_home: "/opt/kibana/{{ kibana_version }}"
```

`kibana_version` - версия `kibana` для установки

`kibana_home` - директория установки `kibana`

### templates

Шаблоны


#### kib.sh.j2

Шаблон с экспортом переменных среды `Kibana`

```bash
# Warning: This file is Ansible Managed, manual changes will be overwritten on next playbook run.
#!/usr/bin/env bash

export KB_HOME={{ kibana_home }}
export PATH=$PATH:$KB_HOME/bin
```

### playbook/inventory

Описание, на каких хостах необходимо выполнять действия

#### prod.yml

```yaml
---
elasticsearch:
  hosts:
    elasticsearch:
      ansible_connection: docker      
kibana:
  hosts:
    kibana:
      ansible_connection: docker
```

У нас 2 хоста, `elasticsearch` и `kibana`. Поднимаются в `docker-compose`.

```yaml
version: "3.9"
services:
  elasticsearch:
    image: pycontribs/ubuntu
    container_name: elasticsearch
    entrypoint: "tail -f /dev/null"

  kibana:
    image: pycontribs/ubuntu
    container_name: kibana
    entrypoint: "tail -f /dev/null"

```

## Playbook

### site.yml

Сам плейбук с 3 ролями

```yaml
---
- name: Install Java
  hosts: all
  roles:
    - java
- name: Install Elasticsearch
  hosts: elasticsearch
  roles:
    - elastic-role
- name: Install Kibana
  hosts: kibana
  roles:
    - kibana_role
```

### Что делается?

#### Java

На всех хостах.

Загрузка локального архива `Oracle JDK` на хосты - `copy`.

Создание директории для `Java` - `file`

Разархивирование архива в директорию - `unarchive`

Экспорт переменных среды из шаблона - `template`

#### Elasticsearch

На хосте `elasticsearch`

Скачивание архива - `get_url`

Создание директории для `Elasticsearch` - `file`

Разархивирование архива в директорию - `unarchive`

Экспорт переменных среды из шаблона - `template`

#### Kibana

На хосте `kibana`

Скачивание архива - `get_url`

Создание директории для `Elasticsearch` - `file`

Разархивирование архива в директорию - `unarchive`

Экспорт переменных среды из шаблона - `template`

#### Теги

`java`,`elastic`,`kibana`.
