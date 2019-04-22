import re
import config as c
from os import path

from telethon import TelegramClient, events

script_dir = path.dirname(path.realpath(__file__))
session_file = path.join(script_dir, c.session_name)

client = TelegramClient(session_file, c.api_id, c.api_hash)

# plugin loading
# plugin reloading
# command decorator
# help
# pin monitor (pin command???)

# Utilities

def titlecase(s):
    """
    Replace the contents of s with the output of titlecase_replace.
    """
    def titlecase_replace(match):
        if match.group(0).islower():
            return match.group(0)[0].upper() + match.group(0)[1:]
        else:
            return match.group(0)
    return re.sub(r'[a-zA-Z]+([\'"a-zA-Z]*)', titlecase_replace, s)

events.is_handler