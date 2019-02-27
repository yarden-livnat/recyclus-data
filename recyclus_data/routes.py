from flask import Blueprint, current_app as app, request, send_file
from flask_restplus import Api, Resource
from webargs.flaskparser import use_args
from pathlib import Path

from .schema import store_args, internal_store_args, list_args, fetch_args
from . import datastore


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Recyclus data service',
          version='1.0',
          description='Remote Cyclus data services api',
          doc='/doc/')


@api.route('/internal/store')
class Store(Resource):
    @use_args(internal_store_args)
    def post(self, args):
        datastore.store(args, request.files)


@api.route('/list')
class User(Resource):
    @use_args(list_args)
    def get(self, args):
        identity = args.pop('identity')
        args['user'] = identity['user']
        return datastore.find(args)


@api.route('/fetch')
class Fetch(Resource):

    @use_args(fetch_args)
    def get(self, args):
        identity = args.pop('identity')
        args['user'] = identity['user']
        try:
            path, name = datastore.fetch(identity['user'], args['jobid'], args['file'])
            return send_file(path, attachment_filename=name)
        except FileNotFoundError:
            return {
                    'message': 'File not found',
                    'user': identity['user'],
                    'jobid': args['jobid'],
                    'filename': args['file']
                   }, 404


# @api.route('/store')
# class Store(Resource):
#     @use_args(store_args)
#     def post(self, args):
#         # identity = args.pop('identity')
#         # if args.get('user') is None:
#         #     args['user'] = identity['user']
#         # elif args.get('user') != identity['user']:
#         #     if identity['roles'] != 'service':
#         #         return {
#         #             'message': 'only services can store files for a user'
#         #         }, 404
#         path = Path('/repository') / args['jobid']
#         path.mkdir(parents=True, exist_ok=True)
#         for name, f in request.files.items():
#             app.logger.debug('fields: %s: %s ', name, f.filename)
#             f.save(str(path / f.filename))

