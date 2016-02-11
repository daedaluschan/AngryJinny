__author__ = 'daedaluschan'
import sys
import time
import telepot
from telepot.delegate import per_chat_id, create_open

from datetime import date
from types import *

class Jinny:
  myName = "Jinny Chan"
  myDOB = date(2015,6,24)

  @staticmethod
  def getNumOfDays():
    currentDate = date.today()
    return (currentDate - Jinny.myDOB).days + 1

  @staticmethod
  def getNumOfDaysSpecific(whichDateIn):
    if type(whichDateIn) is StringType or type(whichDateIn) is UnicodeType:
      whichDate = ""
      for charact in whichDateIn:
        if charact.isdigit():
          whichDate = whichDate + charact
      theDate = date(int(whichDate[0:4]),int(whichDate[4:6]),int(whichDate[6:8]))
    else:
      theDate = whichDateIn

    return (theDate - Jinny.myDOB).days + 1

class AngryJinny(telepot.helper.ChatHandler):
    def __init__(self, seed_tuple, timeout):
        super(AngryJinny, self).__init__(seed_tuple, timeout)
        self._asking_date = False
        print('constructor is being called')

    def on_message(self, msg):
        print('on_message() is being called')
        flavor = telepot.flavor(msg)

        # normal message
        if flavor == 'normal':
            content_type, chat_type, _chat_id = telepot.glance2(msg)
            print('Normal Message:', content_type, chat_type, _chat_id, '; message content: ', msg)

            if msg['text'] == '/start' or msg['text'] == '/today':
                self.sender.sendMessage(text='Today is ' + str(date.today()) + '. \n' +
                                                       'It is my day ' + str(Jinny.getNumOfDays()) + '. \n' +
                                                       'Use /help for more options')
            elif msg['text'] == '/help':
                self.sender.sendMessage(text='/today - get today\'s date and my day count. \n' +
                                                       '/help - for those who have bad memory. \n' +
                                                       '/query - check my day count for a particular date. \n')
            elif msg['text'] == '/query':
                self._asking_date = True
                self.sender.sendMessage(text='Which date ar ?')
            elif msg['text'] == '/No' :
                self._asking_date = False
                self.sender.sendMessage(text='Bye !')
            elif self._asking_date:
                self.sender.sendMessage(text='For ' + msg['text'] + ', It is my day ' +
                                             str(Jinny.getNumOfDaysSpecific(msg['text'])) +
                                             '. Any other date to ask ? /No ?')
            else:
                self.sender.sendMessage(text='I don\'t understand what you are saying !\n' +
                                                       'Try again ! Or use /help for assistance.')
        else:
            raise telepot.BadFlavor(msg)

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(AngryJinny, timeout=30)),])
print('Listening ...')
bot.notifyOnMessage(run_forever=True)

