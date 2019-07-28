import os
import schedule
import time
import logging
from slackclient import SlackClient

import requests
from datetime import datetime
import time

Time = []
Value = []
www = []
LastTimestamp = 0
TimeReal = []
ValueReal = []
wwwReal = []

logging.basicConfig(level=logging.DEBUG)

def insert (source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]

def deleteItem(index):
    Time.pop(index)
    Value.pop(index)
    www.pop(index)

def addReal(index):
    TimeReal.append(Time[index])
    ValueReal.append(Value[index])
    wwwReal.append(www[index])

def sendMessage(slack_client, msg):
  # make the POST request through the python slack client
  updateMsg = slack_client.api_call(
    "chat.postMessage",
    channel='#allgemein',
    text=msg
  )

  # check if the request was a success
  if updateMsg['ok'] is not True:
    logging.error(updateMsg)
  else:
    logging.debug(updateMsg)

if __name__ == "__main__":
    SLACK_BOT_TOKEN = "xoxb-700821962085-709790579735-7a2RLf4jW3Mx8BRaPOFb1ueB"
    slack_client = SlackClient(SLACK_BOT_TOKEN)
    logging.debug("authorized slack client")

    # schedule.every().monday.at("13:15").do(lambda: sendMessage(slack_client, msg))
    logging.info("entering loop")

    LastTimestamp = time.time()
    print(LastTimestamp)
    print(int(LastTimestamp))

    while True:
        r = requests.get('https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0xE477292f1B3268687A29376116B0ED27A9c76170&sort=desc&apikey=JMSGM53AC1ESPHY9WZ38VCJQJ5J47E9USU')
        j = r.json()
        for each in j['result']:
          Time.append(each['timeStamp'])
          Value.append(each['value'])
          www.append(each['hash'])

        for i, val in enumerate(Time):
            if int(val) > int(LastTimestamp):
                if len(Value[i]) > 22:
                    addReal(i)

        print(TimeReal)

        # do sending

        for i, val in enumerate(TimeReal):
            sendMessage(slack_client, "There has been a huge transaction:")
            sendMessage(slack_client, "Zeitpunkt: " + str(datetime.fromtimestamp(int(TimeReal[i]))))
            sendMessage(slack_client, "Wert: " + insert(ValueReal[i], ".", len(ValueReal[i]) - 18))
            sendMessage(slack_client, "www: https://etherscan.io/tx/" + wwwReal[i])
            sendMessage(slack_client, "---------------------------------------------------------------------------\n")

        # reset
        if len(TimeReal) > 0:
            LastTimestamp = max(TimeReal)
        Time.clear()
        Value.clear()
        www.clear()
        TimeReal.clear()
        ValueReal.clear()
        wwwReal.clear()
        time.sleep(5)
