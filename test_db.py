import time
import random
from string import ascii_letters
from pony import orm

db = orm.Database()
db.bind(provider='sqlite', filename=':memory:')

class Group(db.Entity):
    name = orm.PrimaryKey(str)
    collective_noun = orm.Required(str)
    users = orm.Set("User")

class User(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    notify = orm.Required(bool, default=True)
    groups = orm.Set("Group")

db.generate_mapping(create_tables=True)

with orm.db_session:
    User(id=1, name="Kate")
    User(id=2, name="Bob")

    Group(name='H', collective_noun='H')

    Group['H'].users.add(User[1])

    # print(Group["H"].exists(id=1))
    # print(dir(Group['H'].users))
    
    print(User[4] in Group['H'].users)