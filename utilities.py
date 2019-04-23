import re
import time
import logging
import inspect
from collections import defaultdict

import database as db

# Better .title
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

# Cooldown
def cooldown(timeout):
    def wrapper(function):
        last_called = defaultdict(int)

        async def wrapped(event, *args, **kwargs):
            current_time = time.time()
            if current_time - last_called[event.chat_id] < timeout:
                print(last_called)
                time_left = round(timeout - (current_time - last_called[event.chat_id]), 1)
                await log(event, f"Cooldown: {time_left}s")
                return
            last_called[event.chat_id] = current_time
            return await function(event, *args, **kwargs)
        return wrapped
    return wrapper

# Logging
async def log(event, info=""):
    sender = await event.get_sender()
    # Get the name of the command sent to the bot:
    command = inspect.currentframe().f_back.f_code.co_name
    logging.info(
        f"""[{event.date.strftime('%c')}]:
    [{sender.id}]@[{event.chat_id}] {sender.first_name}@{sender.username}: {command}
    {info}""".rstrip())


def get_db_obj(obj, key):
    try:
        return obj[key]
    except db.orm.core.ObjectNotFound:
        pass

def get_group(group_name):
    return get_db_obj(db.Group, group_name)