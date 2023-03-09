import logging,json
import telegram
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import asyncio
from functools import wraps
import api

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator

ACCESS_TOKEN = '6237912476:AAHREjDIVjsHgsoh_FY_pBcuKMLnX6__6P0' 
application = ApplicationBuilder().token(ACCESS_TOKEN).build()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
def command_handler(command):
    def decorator(func):
        handler = CommandHandler(command, func)
        application.add_handler(handler)
        return func
    return decorator

@command_handler("start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
            text='''Hi I'm an anime streaming bot! Search your Favourite anime and watch episodes AdFree With Ease !

Use \help to know and explore more about me and how I work!''')

@command_handler("help")
@send_action(telegram.constants.ChatAction.TYPING)
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    helpMarkup = '''
Bot Usage Guide: 

/start - To Start the Bot.
/search - To Search 
/trending - To get list of trending anime
/animeinfo - To get the info of anime
/watch - To watch a particular anime episode, Please change the suffix of ep no to get next episode link
/help - To get the usage guide
    '''
    await context.bot.send_message(chat_id=update.effective_chat.id,text=helpMarkup)

@command_handler("test")
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = telegram.ReplyKeyboardRemove()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="`test`",parse_mode=telegram.constants.ParseMode.MARKDOWN,reply_markup=reply_markup)

@command_handler("anime")
@send_action(telegram.constants.ChatAction.TYPING)
async def anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    eplnks = [f'\t  <a href = "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx127230-FlochcFsyoF4.png">EP: {i} </a>' for i in range(1,26)]
    await context.bot.send_photo(chat_id=update.effective_chat.id,photo='https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx127230-FlochcFsyoF4.png')
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                    text="".join(eplnks), 
                    parse_mode=telegram.constants.ParseMode.HTML)

@command_handler("search")
@send_action(telegram.constants.ChatAction.TYPING)
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    apires = api.search(' '.join(context.args))
    text = [f'\n {i+1}.`{res.name}`' for i,res in enumerate(apires)]
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                    text="".join(text)+'\n use /animeinfo (anime name) to get the anime detailsdetails',parse_mode=telegram.constants.ParseMode.MARKDOWN)
    
@command_handler("animeinfo")
@send_action(telegram.constants.ChatAction.TYPING)
async def animeinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    apires = api.animeInfo(' '.join(context.args))
    print(apires.getMarkUp())
    # await context.bot.send_message(chat_id=update.effective_chat.id,
    #                                 text = apires.getMarkUp().replace("<br>",""),parse_mode=telegram.constants.ParseMode.HTML)
    await context.bot.send_photo(chat_id=update.effective_chat.id,photo=apires.img,
                                    caption = apires.markup.replace("<br>",""),parse_mode=telegram.constants.ParseMode.MARKDOWN)


@command_handler("watch")
@send_action(telegram.constants.ChatAction.TYPING)
async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    apires = api.getEps(context.args[0])
    await context.bot.send_message(chat_id=update.effective_chat.id,text=f"Watch Here 👉👉👉 <a href='{apires}'>1080p</a>",parse_mode=telegram.constants.ParseMode.HTML)

@command_handler("schedule")
@send_action(telegram.constants.ChatAction.TYPING)
async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sch = api.getSch()
    # await context.bot.send_message(chat_id=update.effective_chat.id,text=)


@command_handler("trending")
@send_action(telegram.constants.ChatAction.TYPING)
async def trending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = api.getTrending()
    await context.bot.send_message(chat_id=update.effective_chat.id,text=''.join(t),parse_mode=telegram.constants.ParseMode.MARKDOWN)

async def main():
    bot = telegram.Bot(ACCESS_TOKEN)
    async with bot:
        # print((await bot.get_updates()))
        custom_keyboard = [['Anime', 'Hentai'], 
                   ['bottom-left', 'bottom-right']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        await bot.send_message(
            chat_id=1095316145, 
            text="Custom Keyboard Test", 
            reply_markup=reply_markup
        )
        await bot.send_message(text='Hi goat',chat_id=1095316145)

if __name__ == '__main__':    
    # start_handler = CommandHandler('start', start)
    # application.add_handler(start_handler)
    
    application.run_polling()
    # asyncio.run(main())
