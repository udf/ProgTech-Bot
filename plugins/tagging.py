import re
import utilities as u
import database as db
from telethon import events

@events.register(events.NewMessage(pattern=re.compile(r"@(\S+)").search))
async def on_tag(event):
    group_name = event.pattern_match.group(1).casefold()
    with db.orm.db_session:
        group = u.get_group(group_name)

        if not group:
            await event.reply(f"{group_name} isn't a group, you kate.")
            return

        return_text =f"Tagging all {group.collective_noun}s!"
        for user in group.users:
            return_text += f"[\u2063](tg://user?id={user.id})"

    await event.reply(return_text)