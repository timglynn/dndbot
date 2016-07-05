FROM	centos:centos7
MAINTAINER	Tim Glynn tim@timglynn.com


#Install EPEL, python
RUN	yum install -y epel-release && yum install -y python python-pip


# Install the slackclient
RUN	pip install slackclient 

ADD	dndbot /usr/local/dndbot/

#Run the bot
CMD	cd /usr/local/dndbot && python ./d_and_d_slackbot.py
