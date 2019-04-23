import re
import logging
import asyncio
import utilities as u
from telethon import events
from telethon.tl.functions.channels import EditTitleRequest
from telethon.errors.rpcerrorlist import ChatNotModifiedError


# Config
original_name = "Programming & Tech"
rename_lock = asyncio.Lock()
revert_time = 2 * 60 * 60


async def edit_title(event, title):
    chat = await event.get_input_chat()
    try:
        await event.client(EditTitleRequest(
            channel=chat, title=title
        ))
    except ChatNotModifiedError:
        pass # Everything is ok

@events.register(events.NewMessage(
    pattern=re.compile(r"(?i)programming (?:&|and) (.+)"),))
@u.cooldown(80)
async def on_name(event):
    new_topic = u.titlecase(event.pattern_match.group(1))
    new_title = f"Programming & {new_topic}"
    if "Tech" not in new_title:
        new_title += " & Tech"

    if len(new_title) > 255:
        return

    with (await rename_lock):
        await edit_title(event, new_title)

    await asyncio.sleep(revert_time)
    await edit_title(event, original_name)
