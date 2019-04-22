from pony import orm

db = orm.Database()
db.bind(provider="sqlite", filename="database.sqlite", create_db=True)


class Group(db.Entity):
    name = orm.PrimaryKey(str)
    collective_noun = orm.Required(str)
    users = orm.Set("User")


class User(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    tg_id = orm.Required(int, unique=True)
    name = orm.Required(str)
    notify = orm.Required(bool, default=True)
    groups = orm.Set("Group")


db.generate_mapping(create_tables=True)