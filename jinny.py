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
    if type(whichDateIn) is StringType:
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
                self.sender.sendMessage(chat_id=_chat_id, text='Today is ' + str(date.today()) + '. \n' +
                                                       'It is Jinny\'s day ' + str(Jinny.getNumOfDays()) + '. \n' +
                                                       'Use /help for more options')
            elif msg['text'] == '/help':
                self.sender.sendMessage(chat_id=_chat_id, text='/today - get today\'s date and Jinny\'s day. \n' +
                                                       '/help - help menu. \n' +
                                                       '/query - check the number of days for a particular date. \n')
            else:
                self.sender.sendMessage(chat_id=_chat_id, text='I don\'t understand what you are saying !\n' +
                                                       'please try again or use /help for assistance.')
        else:
            raise telepot.BadFlavor(msg)

class YourBot(telepot.Bot):
    def handle(self, msg):
        flavor = telepot.flavor(msg)

        # normal message
        if flavor == 'normal':
            content_type, chat_type, chat_id = telepot.glance2(msg)
            print('Normal Message:', content_type, chat_type, chat_id, '; message content: ', msg)

            if msg['text'] == '/start' or msg['text'] == '/today':
                self.sendMessage(chat_id=chat_id, text='Today is ' + str(date.today()) + '. \n' +
                                                       'It is Jinny\'s day ' + str(Jinny.getNumOfDays()) + '. \n' +
                                                       'Use /help for more options')
            elif msg['text'] == '/help':
                self.sendMessage(chat_id=chat_id, text='/today - get today\'s date and Jinny\'s day. \n' +
                                                       '/help - help menu. \n' +
                                                       '/query - check the number of days for a particular date. \n')
            else:
                self.sendMessage(chat_id=chat_id, text='I don\'t understand what you are saying !\n' +
                                                       'please try again or use /help for assistance.')

        # inline query - need `/setinline`
        elif flavor == 'inline_query':
            query_id, from_id, query_string = telepot.glance2(msg, flavor=flavor)
            print('Inline Query:', query_id, from_id, query_string)

            # Compose your own answers
            articles = [{'type': 'article',
                            'id': 'abc', 'title': 'ABC', 'message_text': 'Good morning'}]

            bot.answerInlineQuery(query_id, articles)

        # chosen inline result - need `/setinlinefeedback`
        elif flavor == 'chosen_inline_result':
            result_id, from_id, query_string = telepot.glance2(msg, flavor=flavor)
            print('Chosen Inline Result:', result_id, from_id, query_string)

            # Remember the chosen answer to do better next time

        else:
            raise telepot.BadFlavor(msg)


TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(AngryJinny, timeout=10)),])
bot.notifyOnMessage(run_forever=True)
print('Listening ...')

# Keep the program running.
# while 1:
#     time.sleep(10)