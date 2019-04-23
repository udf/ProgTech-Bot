import re
import logging
from os import path
from pathlib import Path
from importlib import import_module, reload
from inspect import getmembers

from telethon import TelegramClient, events

import database as db
import config as c

logging.basicConfig(level=logging.INFO)
script_dir = path.dirname(path.realpath(__file__))
session_file = path.join(script_dir, c.session_name)

logger = logging.getLogger('main')
client = TelegramClient(session_file, c.api_id, c.api_hash)
plugins = {}

# TODO:
# bot command decorator
#    /command@bot_name
#    args (optional?)
# custom command, with option for command prefixes - ideal for userbots
# delete empty groups
# list all group's users
# Load/unload plugins
# pin command
# help


def get_handlers(module):
    for name, member in getmembers(module):
        if events.is_handler(member):
            yield member


def load_plugin(name):
    with db.orm.db_session:
        if not db.Plugin.exists(name=name):
            db.Plugin(name=name)
        if not db.Plugin[name].enabled:
            logger.info('Not loading disabled plugin ')
            return
    if name in plugins:
        for handler in get_handlers(plugins[name]):
            client.remove_event_handler(handler)
        plugins[name] = reload(plugins[name])
    else:
        plugins[name] = import_module(f'plugins.{name}')
    num_handlers = 0
    for member in get_handlers(plugins[name]):
        num_handlers += 1
        client.add_event_handler(member)
    logger.info("Loaded plugin %s (%d handlers)", name, num_handlers)


@client.on(events.NewMessage(incoming=True, forwards=False))
async def track_users(event):
    """
    Add every new user encountered to the database, if they don't already exist
    """
    user_id = event.from_id
    first_name = event.sender.first_name
    with db.orm.db_session:
        try:
            db.User[user_id].name = first_name # Update user
        except db.orm.core.ObjectNotFound:
            db.User(id=user_id, name=first_name) # Add user


for filepath in Path().glob('./plugins/*.py'):
    name = Path(filepath).stem
    load_plugin(name)

client.start(bot_token=c.bot_token)
client.run_until_disconnected()

# plugin loading func# pin monitor (pin command???)