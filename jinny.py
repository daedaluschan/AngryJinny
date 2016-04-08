# coding=UTF8
__author__ = 'daedaluschan'

import sys, time
import telepot
from telepot.delegate import per_chat_id, create_open

from datetime import date
from types import *
from chk_n_conv import  chkNConv
from enum import Enum

to_buy_list = []
white_list = [161517202]
file_name = 'list.txt'

class ConverType(Enum):
    nothing = 1
    asking_date = 2
    adding_to_buy = 3


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
        self._convert_type = ConverType.nothing
        print('constructor is being called')

    def genKeyboard(self):
        print('generate keyboard')
        show_keyboard = {'keyboard': [[u'今日 day 幾',u'某日係 day 幾'], [u'有乜未買？', u'有野要買']]}

        for idx, item in to_buy_list:
            print(u'買左[' + chkNConv(idx.__str__()) )
            show_keyboard['keyboard'].append([u'買左[' + chkNConv(idx.__str__()) + u']' + chkNConv(item)])
        return show_keyboard

    def genBuyList(self):
        buy_list = u'要買呢D：\n\n'
        for item in to_buy_list:
            buy_list = buy_list + u'- ' + chkNConv(item) + u'\n'

        return buy_list

    def doneWithBuyList(self):
        self.sender.sendMessage(text=u'Bye', reply_markup=self.genKeyboard())
        for white_user in white_list:
            self.bot.sendMessage(white_user, self.genBuyList())

    def writeListToFile(self):
        with open(name=file_name, mode='w') as f:
            for item in to_buy_list:
                f.write(item.encode('utf-8'))
                f.write(u'\n'.encode('utf-8'))
        f.close()



    def on_message(self, msg):
        print('on_message() is being called')
        flavor = telepot.flavor(msg)

        # normal message
        if flavor == 'normal':
            content_type, chat_type, _chat_id = telepot.glance2(msg)
            print('Normal Message:', content_type, chat_type, _chat_id, '; message content: ', msg)

            if _chat_id in white_list :

                if self._convert_type == ConverType.nothing:
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
                        self._convert_type = ConverType.asking_date
                        self.sender.sendMessage(text=u'邊日呀 ?', reply_markup={'hide_keyboard': True})
                    elif chkNConv(msg['text']) == u'/No' :
                        self._convert_type = ConverType.nothing
                        self.sender.sendMessage(text=u'Bye !',
                                                reply_markup=self.genKeyboard())
                    elif chkNConv(msg['text']) == u'有野要買':
                        self._convert_type = ConverType.adding_to_buy
                        self.sender.sendMessage(text=u'買乜？', reply_markup={'hide_keyboard': True})
                    elif chkNConv(msg['text']) == u'有乜未買？':
                        self.sender.sendMessage(text=self.genBuyList(), reply_markup=self.genKeyboard())
                    else:
                        self.sender.sendMessage(text=u'我唔明呀。\n' +
                                                     u'你試多次啦。或者用 /help 我就教你用。')
                elif self._convert_type == ConverType.asking_date:
                    try :
                        self.sender.sendMessage(text=u'For ' + chkNConv(msg['text']) + u', It is my day ' +
                                                     chkNConv(str(Jinny.getNumOfDaysSpecific(msg['text']))) +
                                                     u'. Any other date to ask ? /No ?')
                    except BaseException :
                        self.sender.sendMessage(text=u'Not a data that I can understand ! \n' +
                                                     u'What date (YYYYMMDD) ? \nOr you done ? ( /No )')
                elif self._convert_type == ConverType.adding_to_buy:
                    if chkNConv(msg['text']) == u'/done':
                        self._convert_type = ConverType.nothing
                        self.doneWithBuyList()
                        self.writeListToFile()
                    else:
                        to_buy_list.append(chkNConv(msg['text']))
                        self.sender.sendMessage(text=u'仲有冇？如果冇，就用 /done 完結。', reply_markup={'hide_keyboard': True})
                else:
                    self.sender.sendMessage(text=u'我唔明呀。\n' +
                                                 u'你試多次啦。或者用 /help 我就教你用。')

            else:
                self.sender.sendMessage(text=u'你邊位呀？')
        else:
            raise telepot.BadFlavor(msg)

        print(u'to buy list: ' + self.genBuyList())

TOKEN = sys.argv[1]  # get token from command-line

with open(name=file_name, mode='r') as f:
    lines = f.read().decode('utf-8').splitlines()
f.close()
to_buy_list = lines

bot = telepot.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(AngryJinny, timeout=30)),])
print('Listening ...')
bot.notifyOnMessage(run_forever=True)

