from flask_script import Manager, Server
from flask_migrate import Migrate
from order_app import app, db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port=5000, use_debugger=True))
if __name__ == '__main__':
    manager.run()