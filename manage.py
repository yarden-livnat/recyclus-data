#!/usr/bin/env python
import os
# import unittest
from flask_script import Manager

from recyclus_data import create_app

app = create_app(os.getenv('FLASK_ENV') or 'production')

manager = Manager(app)

@manager.command
def run():
    app.run(host='0.0.0.0', port=5020)


if __name__ == '__main__':
    manager.run()
