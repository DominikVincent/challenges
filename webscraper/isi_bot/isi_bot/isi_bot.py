import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from isi_bot.isi_bot.utils import read_config
from isi_bot.game_watcher.game_watcher import get_spielberichte_url, get_spielberichte_content, get_all_spiele
import time
from telegram.error import RetryAfter, TimedOut
from datetime import datetime
import schedule
import threading
import os
import json
import asyncio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class Isi_bot():
    def __init__(self, config_path="data/config.json"):
        self.config = read_config(config_path)

        self.state = State(self.config["state_path"])
        with self.state as state:
            print(state)

        self.application = ApplicationBuilder().token(self.config["bot_token"]).read_timeout(20).build()

        start_handler = CommandHandler('start', self.start)
        self.application.add_handler(start_handler)

        all_games_handler = CommandHandler('all_games', self.all_games)
        self.application.add_handler(all_games_handler)

        next_games_handler = CommandHandler('next_games', self.next_games)
        self.application.add_handler(next_games_handler)

        activate_game_checking_handler = CommandHandler('activate_game_checking', self.activate_game_checking)
        self.application.add_handler(activate_game_checking_handler)

        remove_game_checking_handler = CommandHandler('remove_game_checking', self.remove_game_checking)
        self.application.add_handler(remove_game_checking_handler)

        # TODO publish available commands


    def run(self):
        loop = asyncio.get_event_loop()
        print("got loop")
        loop.create_task(self.run_schedule())
        print("created task")
        # loop.run_forever()
        # print("run forever")
        self.application.run_polling()
        print("run polling")

    async def run_schedule(self):
        while True:
            await self.check_for_new_game()
            # TODO add times 60
            await asyncio.sleep(self.config["game_polling_interval_min"])

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = "I am the isi game bot. I can report the latest table tennis game results of Isi."
        await self.send_message(context.bot, update.effective_chat.id, message)

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

    
    async def check_for_new_game(self):
        logging.info("Checking for new games ")
        with self.state as state:
            for chat_id in state["chat_ids"].keys():
                await self.send_message(self.application.bot, int(chat_id), "Checking for new games...")

    async def activate_game_checking(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(type(update.effective_chat.id))
        logging.info("Add game checking for chat_id: %d", update.effective_chat.id)
        # add chat_id to state
        with self.state as state:
            state["chat_ids"][update.effective_chat.id] = ""
        
    async def remove_game_checking(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.info("Remove game checking for chat_id: %d", update.effective_chat.id)
        # remove chat_id from state
        with self.state as state:
            # remove chat_id from state
            if str(update.effective_chat.id) in state["chat_ids"]:
                del state["chat_ids"][str(update.effective_chat.id)]
class State():
    def __init__(self, save_path="data/state.json"):
        self.save_path = save_path
        
        # Holds information like in which chats the bot is active, what games have been published already, etc.
        self.state_lock = threading.Lock()
        self.state = {}

        # load state from file
        if os.path.exists(save_path):
            self._load()
        else:
            self.state = {
                "chat_ids": {},
                # the list of send games
                "processed_games": {},
            }
            self._save()
    
    def _load(self):
        if os.path.exists(self.save_path):
            logging.info("Loading state from %s", self.save_path)
            with open(self.save_path, "r") as f:
                self.state = json.load(f)
        else:
            logging.warn("No state file found at %s", self.save_path)
            return False
        return True

    def _save(self):
        logging.info("Saving state to %s", self.save_path)
        with open(self.save_path, "w") as f:
            json.dump(self.state, f)

    def __enter__(self):
        self.state_lock.acquire()
        return self.state

    def __exit__(self, exc_type, exc_value, traceback):
        self._save()
        self.state_lock.release()
