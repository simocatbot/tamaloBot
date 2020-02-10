import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from arranger import arrange_scores
from random import randint
import datetime

#-------------------Logging--------------------#
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#-------------------States---------------------#

PLAYERS, RULE = range(2)

#-----------Define CallBack Functions----------#
def start(update, context):
    buttons = [['3'],['4'],['5'],['6']]
    markup = ReplyKeyboardMarkup(buttons, one_time_keyboard= True)
    logger.info('USER: {}. MESSAGE: {}'.format(update.effective_user.username, update.effective_message.text))
    user = update.effective_user.username
    reply = 'Ciao {}. La parita di Tamalo è ufficialmente iniziata.\nBuona fortuna a tutti i partecipanti.\nQuanti giocatori siete?'.format(user.upper())
    update.message.reply_text(reply, reply_markup = markup)

    return PLAYERS

def players(update, context):
    buttons = [['SI!'],['NO!']]
    markup = ReplyKeyboardMarkup(buttons, one_time_keyboard= True)
    logger.info('USER: {}. MESSAGE: {}'.format(update.effective_user.username, update.effective_message.text))
    text = update.effective_message.text
    reply = 'Bene, avete seguito la prima regola tutti e {}?'.format(text)
    update.message.reply_text(reply, reply_markup = markup)

    return RULE

def rule(update, context):
    rule.now = datetime.datetime.now()
    text = update.effective_message.text
    user = update.effective_user.username
    logger.info('USER: {}. MESSAGE: {}'.format(update.effective_user.username, update.effective_message.text))
    if text =='SI!':
        reply = 'Oooooooookey, {}! Inizia la bisca!\nOre: {}'.format(user.upper(), rule.now.strftime('%H:%M:%S'))
    else:
        reply = 'Mi dispiace {}.\nNon si può giocare a Tamalo se non si seguono le regole!'.format(user.upper())
    update.message.reply_text(reply, reply_markup = ReplyKeyboardRemove())

    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('La bisca sarà per un altro giorno, MELLON!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def mossa(update, context):
    lista_mosse = ['COPPIONA!', 'POZIONI!', 'OPEN LOCK!', 'CLOSED LOCK!', 'TWIN TOWERS!', 'VOOOOLPE!', 'RATTO DELLE SABINE']
    logger.info('USER: {}. MESSAGE: {}'.format(update.effective_user.username, update.effective_message.text))
    update.message.reply_text(lista_mosse[randint(0,len(lista_mosse)-1)])

def scores(update, context):
    text = update.effective_message.text
    logger.info('USER: {}. MESSAGE: {}'.format(update.effective_user.username, update.effective_message.text))
    update.message.reply_text(arrange_scores(text))

def end(update, context):
    now = datetime.datetime.now()
    logger.info('USER: {}. MESSAGE: {}'.format(update.effective_user.username, update.effective_message.text))
    reply = 'Ore: {}. La partita di tamalo è terminata.\n'.format(now.strftime('%H:%M:%S'))
    durata = (now - rule.now).total_seconds()
    minuti = divmod(durata, 60)[0]
    secondi = divmod(durata, 60)[1]
    reply += 'Durata: {} minuti e {} secondi.'.format(int(minuti), round(secondi,2))
    update.message.reply_text(reply)


#-------Main Program, register Handlers--------#
def main():

    token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    updater = Updater(token, use_context= True)
    dp = updater.dispatcher

    conv_hand = ConversationHandler( 
        entry_points= [CommandHandler('start', start)],

        states= {

            PLAYERS: [MessageHandler(Filters.regex('^(3|4|5|6)$'), players)],

            RULE: [MessageHandler(Filters.regex('^(SI!|NO!)$'), rule)]
        },

        fallbacks= [CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_hand)
    dp.add_handler(MessageHandler(Filters.text, scores))
    dp.add_handler(CommandHandler('mossa', mossa))
    dp.add_handler(CommandHandler('end', end))
    
    updater.start_polling(poll_interval= 1.5, timeout= 10)
    updater.idle()

#----------------Pythonic Start----------------#
if __name__ == "__main__":
    main()