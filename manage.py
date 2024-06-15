from flask_script import Manager
import app
from app.scripts.db import InitDB


if __name__ == "__main__":
    manager = Manager(app.create_app())
    manager.add_command('init_db', InitDB())
    manager.run()