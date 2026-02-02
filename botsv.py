from telegram.ext import Updater, CommandHandler, MessageHandler, Filters  
  
# Функция-обработчик команды /start  
def start(update, context):  
    update.message.reply_text('Привет! Я простой бот. Напиши мне /help, чтобы узнать больше.')  
  
# Функция-обработчик всех остальных сообщений  
def echo(update, context):  
    update.message.reply_text(update.message.text)  
  
def main():  
    # Вставьте ваш токен здесь  
    updater = Updater("8428248801:AAGoNtlYsIxlyogUET_xIA_anPyWITBgOFg", use_context=True)  
  
    dp = updater.dispatcher  
  
    dp.add_handler(CommandHandler("start", start))  
    dp.add_handler(MessageHandler(Filters.all, echo))  
  
    updater.start_polling()  
    updater.idle()  
  
if __name__ == '__main__':  
    main()  
