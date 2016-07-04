#!/usr/bin/env python

import random
from slackclient import SlackClient
import time
from supporting_functions import parseInput, rollSomeDie, getDieResult,\
    buildWeaponDictFromFile, getAllWeaponTypes


# Insert slack token
slack_token = ""
slack_conn = SlackClient(slack_token)

# Insert bot ID
at_bot = ""




def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and at_bot in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(at_bot)[1].strip().lower(), \
                       output['channel']
    return None, None




if __name__ == "__main__":
    if slack_conn.rtm_connect():
        backoff_time = 1
        while True:
            command, channel = parse_slack_output(slack_conn.rtm_read())
            if command and channel:
                # DEBUG
              #  print(command)
                
                response = parseInput(command)
                slack_conn.api_call("chat.postMessage", channel=channel,
                    text = response, as_user=True)
            time.sleep(backoff_time)
    else:
        print("Unable to connect")
