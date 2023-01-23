import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from isi_bot.isi_bot.utils import read_config
from isi_bot.game_watcher.game_watcher import get_spielberichte_url, get_spielberichte_content, get_all_spiele
import time
from telegram.error import RetryAfter, TimedOut
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class Isi_bot():
    def __init__(self, config_path="data/config.json"):
        self.config = read_config(config_path)

        self.application = ApplicationBuilder().token(self.config["bot_token"]).read_timeout(20).build()

        start_handler = CommandHandler('start', self.start)
        self.application.add_handler(start_handler)

        all_games_handler = CommandHandler('all_games', self.all_games)
        self.application.add_handler(all_games_handler)

        next_games_handler = CommandHandler('next_games', self.next_games)
        self.application.add_handler(next_games_handler)


    def run(self):
        self.application.run_polling()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = "I am the isi game bot. I can report the latest table tennis game results of Isi."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    async def all_games(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        spielberichte_urls = get_spielberichte_url(self.config["caching"])
        spiele = get_spielberichte_content(spielberichte_urls)
        print(len(spiele))
        for spiel in spiele:
            logging.info("Sending message to chat_id: %d, msg: %s", update.effective_chat.id, str(spiel))
            await self.send_message(context.bot, update.effective_chat.id, str(spiel))

            for i, game in enumerate(spiel.get_games()):
                message = f"Spiel {i+1}: \n"+ str(game)
                await self.send_message(context.bot, update.effective_chat.id, message)

    async def send_message(self, bot, chat_id, message):
        tries = 0
        while tries < 3:
            try:
                logging.info("Sending message (try: %d) to chat_id: %d. Msg: %s", tries, chat_id, message)
                await bot.send_message(chat_id=chat_id, parse_mode="markdown", text=message,
                    connect_timeout=10, read_timeout=20, write_timeout=10)
                return True
            except TimedOut as e:
                logging.warn("Message %s got exception %s", message, e)
                time.sleep(self.config["resend_delay_s"])
                tries += 1
            except RetryAfter as e:
                logging.warn("Message %s got exception %s", message, e)
                time.sleep(e.retry_after + 4)
                tries += 1
        return False

    async def next_games(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        all_games = get_all_spiele()
        # filter out all games after today
        now = datetime.now()
        next_games = [game for game in all_games if game["datetime"] > now]
        
        # for the next 4 games
        next_games = next_games[:self.config["next_games_count"]]
        header_message = f"Die nächsten {self.config['next_games_count']} Spiele:\n"
        message = "\n".join([str(game) for game in next_games])
        await self.send_message(context.bot, update.effective_chat.id, header_message+message)