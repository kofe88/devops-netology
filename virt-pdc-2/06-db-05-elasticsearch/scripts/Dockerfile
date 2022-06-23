FROM centos:7

LABEL ElasticSearch Netology kofe88
ENV ES_HOME elasticsearch

ENV JAVA_HOME /elasticsearch/jdk/

ENV PATH=/usr/lib:/usr/lib/jvm/jre-11/bin:/elasticsearch/bin:$PATH

RUN yum update -y && yum upgrade -y

RUN yum install -y java-11-openjdk wget curl perl-Digest-SHA

RUN cd /home \
    && wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.2.3-linux-x86_64.tar.gz \
    && wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.2.3-linux-x86_64.tar.gz.sha512

RUN cd /home && \
    shasum -a 512 -c elasticsearch-8.2.3-linux-x86_64.tar.gz.sha512 \
    && tar -xzf elasticsearch-8.2.3-linux-x86_64.tar.gz \
    && mv elasticsearch-8.2.3 /elasticsearch


ADD elasticsearch.yml /elasticsearch/config/elasticsearch.yml


RUN groupadd elasticsearch \
    && useradd -g elasticsearch elasticsearch
RUN chown -R elasticsearch:elasticsearch /elasticsearch
RUN mkdir /var/lib/logs \
    && mkdir /var/lib/logs/elasticsearch \
    && chown elasticsearch:elasticsearch /var/lib/logs/elasticsearch
RUN mkdir /var/lib/data \
    && mkdir /var/lib/data/elasticsearch \
    && chown elasticsearch:elasticsearch /var/lib/data/elasticsearch
RUN mkdir /elasticsearch/snapshots \
    && chown elasticsearch:elasticsearch /elasticsearch/snapshots
    

USER elasticsearch
CMD ["elasticsearch"]


