FROM	centos:centos7
MAINTAINER	Tim Glynn tim@timglynn.com


#Install EPEL, python and redis
RUN	yum install -y epel-release && yum install -y python python-pip redis


# Install the slackclient, beautiful soup and redis
RUN	pip install slackclient bs4 redis

ADD	dndbot /usr/local/dndbot/
ADD redis.conf /etc/redis.conf

#Run the bot
CMD	 /usr/bin/redis-server /etc/redis.conf && cd /usr/local/dndbot && python ./d_and_d_slackbot.py
