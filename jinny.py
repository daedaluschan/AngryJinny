# coding=UTF8
__author__ = 'daedaluschan'

import sys, time
import telepot
from telepot.delegate import per_chat_id, create_open

from datetime import date
from types import *
from chk_n_conv import  chkNConv
from enum import Enum

class ConverType(Enum):
    nothing = 1
    create_poll = 2

class Jinny:
  myName = u'Jinny Chan'
  myDOB = date(2015,6,24)

  @staticmethod
  def getNumOfDays():
    currentDate = date.today()
    return (currentDate - Jinny.myDOB).days + 1

  @staticmethod
  def getNumOfDaysSpecific(whichDateIn):
    if type(whichDateIn) is StringType or type(whichDateIn) is UnicodeType:
      whichDate = u''
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
        self.to_buy_list = []
        print('constructor is being called')

    @property
    def to_buy_list(self):
        return self._to_buy_list

    @to_buy_list.setter
    def to_buy_list(self, value):
        self._to_buy_list = value

    def genKeyboard(self):
        print('generate keyboard')
        show_keyboard = {'keyboard': [[u'今日 day 幾',u'某日係 day 幾'], [u'有乜未買？', u'有野要買']]}
        return show_keyboard

    def on_message(self, msg):
        print('on_message() is being called')
        flavor = telepot.flavor(msg)

        # normal message
        if flavor == 'normal':
            content_type, chat_type, _chat_id = telepot.glance2(msg)
            print('Normal Message:', content_type, chat_type, _chat_id, '; message content: ', msg)

            if chkNConv(msg['text']) == u'/start' or chkNConv(msg['text']) == u'/today' or chkNConv(msg['text']) == u'今日 day 幾':
                self.sender.sendMessage(text=u'Today is ' + chkNConv(str(date.today())) + u'. \n' +
                                                       u'It is my day ' + chkNConv(str(Jinny.getNumOfDays())) + u'. \n' +
                                                       u'Use /help for more options',
                                        reply_markup=self.genKeyboard())
            elif chkNConv(msg['text']) == u'/help':
                self.sender.sendMessage(text=u'/today - get today\'s date and my day count. \n' +
                                                       u'/help - for those who have bad memory. \n' +
                                                       u'/query - check my day count for a particular date. \n',
                                        reply_markup=self.genKeyboard())
            elif chkNConv(msg['text']) == u'/query' or chkNConv(msg['text']) == u'某日係 day 幾':
                self._asking_date = True
                self.sender.sendMessage(text=u'Which date ar ?', reply_markup={'hide_keyboard': True})
            elif chkNConv(msg['text']) == u'/No' :
                self._asking_date = False
                self.sender.sendMessage(text=u'Bye !',
                                        reply_markup=self.genKeyboard())
            elif self._asking_date:
                try :
                    self.sender.sendMessage(text=u'For ' + chkNConv(msg['text']) + u', It is my day ' +
                                                 chkNConv(str(Jinny.getNumOfDaysSpecific(msg['text']))) +
                                                 u'. Any other date to ask ? /No ?')
                except BaseException :
                    self.sender.sendMessage(text=u'Not a data that I can understand ! \n' +
                                                 u'What date (YYYYMMDD) ? \nOr you done ? ( /No )')
            else:
                self.sender.sendMessage(text=u'I don\'t understand what you are saying !\n' +
                                                       u'Try again ! Or use /help for assistance.')
        else:
            raise telepot.BadFlavor(msg)

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(AngryJinny, timeout=30)),])
print('Listening ...')
bot.notifyOnMessage(run_forever=True)

