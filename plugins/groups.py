import utilities as u
import database as db
from telethon import events



@events.register(events.NewMessage(pattern=r"/create @?(\S+) (\S+)$"))
async def on_create(event):
    group_name = event.pattern_match.group(1).casefold()
    collective_noun = event.pattern_match.group(2).casefold()
    group = u.get_group(group_name)

    if not group:
        # create group
        with db.orm.db_session:
            db.Group(name=group_name, collective_noun=collective_noun)
        await event.reply(
            f"Created `{group_name}`!\n"
            f"Use `/join {group_name}` to join.")
    else:
        await event.reply(
            f"The group `{group_name}` already exists.\n"
            f"Use `/join {group_name}` to join.")


@events.register(events.NewMessage(pattern=r"/edit @?(\S+) (\S+)$"))
async def on_edit(event):
    group_name = event.pattern_match.group(1).casefold()
    collective_noun = event.pattern_match.group(2).casefold()
    group = u.get_group(group_name)

    if not group:
        await event.reply(
            f"The group `{group_name}` does not exist!\n"
            f"Use `/create {group_name} [collective_noun]` to create it.")
        return
    if group.collective_noun == collective_noun:
        await event.reply(
            f"It was already called {collective_noun}.\n"
            "You're such a kate")
        return

    with db.orm.db_session:
        group.collective_noun = collective_noun
    await event.reply(f"Renamed to {collective_noun}.")


@events.register(events.NewMessage(pattern=r"/join @?(\S+)$", forwards=False))
async def on_join(event):
    group_name = event.pattern_match.group(1).casefold()

    with db.orm.db_session:
        group = u.get_group(group_name)
        if not group:
            await event.reply(
                f"No group found called `{group_name}`.\n"
                f"Use `/create {group_name} collective_noun` to create it.")
            return

        user = db.User[event.sender_id]
        if user in group.users:
            await event.reply(
                f"You are already a member of `{group_name}`!\n"
                "You're such a kate...")
        else:
            group.users.add(user)
            await event.reply(f"You are now a {group.collective_noun}!")


@events.register(events.NewMessage(pattern=r"/leave @?(\S+)$", forwards=False))
async def on_leave(event):
    group_name = (event.pattern_match.group(1)).casefold()

    group = u.get_group(group_name)
    if not group:
        await event.reply(f"No group found called `{group_name}`.")
        return

    user = db.User[event.sender_id]
    if user in group.users:
        group.users.remove(user)
        await event.reply(
            f"You are no longer a {group.collective_noun}!\n"
            "You are now a kate!")
    else:
        await event.reply(
            f"You aren't a member of `{group_name}`.\n"
            "You're such a kate...")
