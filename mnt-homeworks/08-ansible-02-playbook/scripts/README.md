# 08-ansible-02-playbook
08-ansible-02-playbook

## Описание

Данный плейбук разворачивает на хостах `kibana` и `elascticsearch` соответствующие сервисы и `Oracle jdk`

`Oracle jdk` необходимо поместить в папку `files` в формате `.tar.gz` предварительно скачав с официального сайта.

`Kibana` и `Elasticsearch` скачиваются напрямую с сайтов разработчиков ( нужен VPN для РФ)

## Параметры

### playbook/group_vars

В каталогах расположены переменные для соответствующих хостов.

#### all

Для всех хостов. 

`vars.yml`

```yaml
---
java_jdk_version: 11.0.16
java_oracle_jdk_package: jdk-11.0.16_linux-x64_bin.tar.gz
```

`java_jdk_version` - версия JDK для установки

`java_oracle_jdk_package` - имя пакета, скачиваемого с оф. сайта

#### elasticsearch

Для хоста `elasticsearch`. 

`vars.yml`

```yaml
---
elastic_version: "8.3.3"
elastic_home: "/opt/elastic/{{ elastic_version }}"
```

`elastic_version` - версия `elasticsearch` для установки

`elastic_home` - директория установки `elasticsearch`

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

### playbook/templates

Шаблоны

#### elk.sh.j2

Шаблон с экспортом переменных среды `Elasticsearch`

```bash
# Warning: This file is Ansible Managed, manual changes will be overwritten on next playbook run.
#!/usr/bin/env bash

export ES_HOME={{ elastic_home }}
export PATH=$PATH:$ES_HOME/bin
```

#### jdk.sh.j2

Шаблон с экспортом переменных среды `Oracle JDK`

```bash
# Warning: This file is Ansible Managed, manual changes will be overwritten on next playbook run.
#!/usr/bin/env bash

export JAVA_HOME={{ java_home }}
export PATH=$PATH:$JAVA_HOME/bin
```

#### elk.sh.j2

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

Сам плейбук с плеями

```yaml
---
- name: Install Java
  hosts: all
  tasks:
    - name: Set facts for Java 11 vars
      set_fact:
        java_home: "/opt/jdk/{{ java_jdk_version }}"
      tags: java
    - name: Upload .tar.gz file containing binaries from local storage
      copy:
        src: "{{ java_oracle_jdk_package }}"
        dest: "/tmp/jdk-{{ java_jdk_version }}.tar.gz"
        mode: 0755
      register: download_java_binaries
      until: download_java_binaries is succeeded
      tags: java
    - name: Ensure installation dir exists
      become: true
      file:
        state: directory
        path: "{{ java_home }}"
        mode: 0755
      tags: java
    - name: Extract java in the installation directory
      become: true
      unarchive:
        copy: false
        src: "/tmp/jdk-{{ java_jdk_version }}.tar.gz"
        dest: "{{ java_home }}"
        extra_opts: [--strip-components=1]
        creates: "{{ java_home }}/bin/java"
        mode: 0755
      tags:
        - java
    - name: Export environment variables
      become: true
      template:
        src: jdk.sh.j2
        dest: /etc/profile.d/jdk.sh
        mode: 0755
      tags: java
- name: Install Elasticsearch
  hosts: elasticsearch
  tasks:
    - name: Upload tar.gz Elasticsearch from remote URL
      get_url:
        url: "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{ elastic_version }}-linux-x86_64.tar.gz"
        dest: "/tmp/elasticsearch-{{ elastic_version }}-linux-x86_64.tar.gz"
        mode: 0755
        timeout: 60
        force: true
        validate_certs: false
      register: get_elastic
      until: get_elastic is succeeded
      tags: elastic
    - name: Create directrory for Elasticsearch
      file:
        state: directory
        path: "{{ elastic_home }}"
        mode: 0755
      tags: elastic
    - name: Extract Elasticsearch in the installation directory
      become: true
      unarchive:
        copy: false
        src: "/tmp/elasticsearch-{{ elastic_version }}-linux-x86_64.tar.gz"
        dest: "{{ elastic_home }}"
        extra_opts: [--strip-components=1]
        creates: "{{ elastic_home }}/bin/elasticsearch"
        mode: 0755
      tags:
        - elastic
    - name: Set environment Elastic
      become: true
      template:
        src: templates/elk.sh.j2
        dest: /etc/profile.d/elk.sh
        mode: 0755
      tags: elastic
- name: Install Kibana
  hosts: kibana
  tasks:
    - name: Upload tar.gz Kibana from remote URL
      get_url:
        url: "https://artifacts.elastic.co/downloads/kibana/kibana-{{ kibana_version }}-linux-x86_64.tar.gz"
        dest: "/tmp/kibana-{{ kibana_version }}-linux-x86_64.tar.gz"
        mode: 0755
        timeout: 60
        force: true
        validate_certs: false
      register: get_kibana
      until: get_kibana is succeeded
      tags: kibana
    - name: Create directrory for Kibana
      file:
        state: directory
        path: "{{ kibana_home }}"
        mode: 0755
      tags: kibana
    - name: Extract Kibana in the installation directory
      become: true
      unarchive:
        copy: false
        src: "/tmp/kibana-{{ kibana_version }}-linux-x86_64.tar.gz"
        dest: "{{ kibana_home }}"
        extra_opts: [--strip-components=1]
        creates: "{{ kibana_home }}/bin/kibana"
        mode: 0755
      tags:
        - kibana
    - name: Set environment Kibana
      become: true
      template:
        src: templates/kib.sh.j2
        dest: /etc/profile.d/kib.sh
        mode: 0755
      tags: kibana
```

### Что делается?

#### Java

На всех хостах.

Установка переменной - `set fact`

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
