import utilities as u
from datetime import datetime
from telethon import events

# /ping
@events.register(events.NewMessage(pattern=r"/ping$"))
async def ping_pong(event):
    if event.is_private:
        a = datetime.timestamp(datetime.now())
        message = await event.reply("**Pong!**")
        b = datetime.timestamp(datetime.now()) - a
        await u.log(event, f"{b:.3f}")
await message.edit(f"**Pong!**\nTook `{b:.3f}` seconds")