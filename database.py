from pony import orm

db = orm.Database()
db.bind(provider="sqlite", filename="database.sqlite", create_db=True)


class Plugin(db.Entity):
    name = orm.PrimaryKey(str)
    enabled = orm.Required(bool, default=True)


class Group(db.Entity):
    name = orm.PrimaryKey(str)
    collective_noun = orm.Required(str)
    users = orm.Set("User", lazy=True)


class User(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(str)
    notify = orm.Required(bool, default=True)
    groups = orm.Set("Group")


db.generate_mapping(create_tables=True)