from isi_bot.isi_bot.utils import read_config
from isi_bot.game_watcher.game_watcher import get_spielberichte_url, get_spielberichte_content, get_all_spiele

from telegram import Update, BotCommand
from telegram.ext import     Application, ApplicationBuilder, ContextTypes, CommandHandler
from telegram.error import RetryAfter, TimedOut

import logging
import time
from datetime import datetime
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

        self.application = ApplicationBuilder().token(
            self.config["bot_token"]).read_timeout(20) \
            .post_init(self.setup).build()

        start_handler = CommandHandler('start', self.start)
        self.application.add_handler(start_handler)

        all_games_handler = CommandHandler('all_games', self.all_spiele)
        self.application.add_handler(all_games_handler)

        next_games_handler = CommandHandler('next_games', self.next_spiele)
        self.application.add_handler(next_games_handler)

        activate_game_checking_handler = CommandHandler(
            'activate_game_checking', self.activate_game_checking)
        self.application.add_handler(activate_game_checking_handler)

        remove_game_checking_handler = CommandHandler(
            'remove_game_checking', self.remove_game_checking)
        self.application.add_handler(remove_game_checking_handler)

        self.commands = [
            BotCommand(command="/start", description="Startet den bot"),
            BotCommand(command="/all_games", description="Gibt alle Spiel Ergebnisse aus"),
            BotCommand(command="/next_games", description="Gibt die nächsten Spiele aus"),
            BotCommand(command="/activate_game_checking", description="Aktiviert die automatische Spiel Ergebnis Benachrichtigung"),
            BotCommand(command="/remove_game_checking", description="Deaktiviert die automatische Spiel Ergebnis Benachrichtigung"),
        ]

    async def setup(self, application: Application):
        await self.application.bot.set_my_commands(self.commands)

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
            await self.check_for_new_spiele()
            await asyncio.sleep(self.config["game_polling_interval_min"]*60)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = "I am the isi game bot. I can report the latest table tennis game results of Isi."
        await self.send_message(context.bot, update.effective_chat.id, message)

    async def send_spiele(self, spiele, chat_id):
        for spiel in spiele:
            logging.info("Sending message to chat_id: %d, msg: %s",
                         chat_id, str(spiel))
            await self.send_message(self.application.bot, chat_id, str(spiel))

            for i, game in enumerate(spiel.get_games()):
                message = f"Spiel {i+1}: \n" + str(game)
                await self.send_message(self.application.bot, chat_id, message)

    async def all_spiele(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        spielberichte_urls = get_spielberichte_url(self.config["caching"])
        spiele = get_spielberichte_content(spielberichte_urls)
        await self.send_spiele(spiele, update.effective_chat.id)

    async def send_message(self, bot, chat_id, message):
        tries = 0
        while tries < 3:
            try:
                logging.info(
                    "Sending message (try: %d) to chat_id: %d. Msg: %s", tries, chat_id, message)
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

    async def next_spiele(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        all_games = get_all_spiele()
        # filter out all games after today
        now = datetime.now()
        next_games = [game for game in all_games if game["datetime"] > now]

        # for the next 4 games
        next_games = next_games[:self.config["next_games_count"]]
        header_message = f"Die nächsten {self.config['next_games_count']} Spiele:\n"
        message = "\n".join([str(game) for game in next_games])
        await self.send_message(context.bot, update.effective_chat.id, header_message+message)

    async def check_for_new_spiele(self):
        logging.info("Checking for new games ")
        spielberichte_urls = get_spielberichte_url(offline=False)

        with self.state as state:
            spielberichte_urls = [
                url for url in spielberichte_urls if url not in state["processed_spiele_urls"]]
            chat_ids = state.get_chat_ids()
            # extent the dict state["processed_spiele_urls"] with the new spielberichte_urls
            for url in spielberichte_urls:
                state["processed_spiele_urls"][url] = ""

        logging.info("Found %d new games sending to %d subscribers",
                     len(spielberichte_urls), len(chat_ids))
        if len(spielberichte_urls) > 0:
            for chat_id in chat_ids:
                msg = "Es gibt ein neues Spielergebnis!" if len(
                    spielberichte_urls) == 1 else f"Es gibt {len(spielberichte_urls)} neue Spielergebnisse!"
                await self.send_message(self.application.bot, chat_id, msg)
        spiele = get_spielberichte_content(spielberichte_urls)
        for chat_id in chat_ids:
            await self.send_spiele(spiele, int(chat_id))

    async def activate_game_checking(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(type(update.effective_chat.id))
        logging.info("Add game checking for chat_id: %d",
                     update.effective_chat.id)
        # add chat_id to state
        with self.state as state:
            state["chat_ids"][update.effective_chat.id] = ""

    async def remove_game_checking(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.info("Remove game checking for chat_id: %d",
                     update.effective_chat.id)
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
                "processed_spiele_urls": {},
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
            json.dump(self.state, f, indent=4)

    def get_chat_ids(self):
        return [int(chat_id) for chat_id in self.state["chat_ids"].keys()]

    def __getitem__(self, item):
        return self.state[item]

    def __enter__(self):
        self.state_lock.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._save()
        self.state_lock.release()
