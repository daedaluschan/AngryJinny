__author__ = 'daedaluschan'
import sys
import time
import telepot


class YourBot(telepot.Bot):
    def handle(self, msg):
        flavor = telepot.flavor(msg)

        # normal message
        if flavor == 'normal':
            content_type, chat_type, chat_id = telepot.glance2(msg)
            print('Normal Message:', content_type, chat_type, chat_id)

            self.sendMessage(chat_id=chat_id, text='Sorry, there are lmiited words I can understand please try again or use /help for assistance.')

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

bot = YourBot(TOKEN)
bot.notifyOnMessage()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)