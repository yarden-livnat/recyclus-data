from flask import current_app as app
from flask_pymongo import PyMongo
import json
from pathlib import Path
import shutil
import uuid


files_dir = Path('/files')

mongo = PyMongo()


def create_path():
    return files_dir / uuid.uuid4().hex


def store(args, files):
    path = create_path()
    path.mkdir(parents=True)

    record = {
        'user': args['user'],
        'name': args['name'],
        'jobid': args['jobid'],
        'path': str(path),
        'files': [f.filename for f in files.values()]
    }

    mongo.db.files.insert_one(record)

    for f in files.values():
        f.save(str(path / f.filename))


def find(args):
    fields = ['user', 'name', 'jobid', 'files']
    results = [dict([(name, value) for name, value in entry.items() if name in fields])
               for entry in mongo.db.files.find(args)]
    return results


def fetch(user, jobid, filename):
    record = mongo.db.files.find_one({'user': user, 'jobid': jobid, 'files': filename})
    if record:
        return str(Path(record['path']) / filename), filename
    raise FileNotFoundError


def delete(args):
    app.logger.debug('delete %s', json.dumps(args))
    records = mongo.db.files.find(args)
    for record in records:
        try:
            app.logger.debug(f'delete directory {record["path"]}')
            shutil.rmtree(record["path"])
        except OSError as e:
            app.logger.error(f'Error: {e.filename}  - {e.strerror}')

    mongo.db.files.delete_many(args)
