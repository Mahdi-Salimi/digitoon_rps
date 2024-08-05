from models import User, Match

User.create_table()
User.migrate()
Match.create_table()
Match.migrate()