from flask import Blueprint, current_app as app, request, send_file
from flask_restplus import Api, Resource
from webargs.flaskparser import use_args

from .schema import store_args, internal_delete_args, internal_store_args, list_args, fetch_args
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


@api.route('/internal/delete')
class InternalDelete(Resource):
    @use_args(internal_delete_args)
    def delete(self, args):
        app.logger.debug('internal delete')
        datastore.delete(args)


@api.route('/files')
class User(Resource):
    @use_args(list_args)
    def get(self, args):
        try:
            identity = args.pop('identity')
            args['user'] = identity['user']
            return datastore.find(args)
        except Exception as e:
            return {
                'message': str(e)
            }, 500


@api.route('/fetch')
class Fetch(Resource):

    @use_args(fetch_args)
    def get(self, args):
        identity = args.pop('identity')
        args['user'] = identity['user']
        try:
            path, name = datastore.fetch(identity['user'], args['jobid'], args['filename'])
            return send_file(path, attachment_filename=name)
        except FileNotFoundError:
            return {
                    'message': 'File not found',
                    'user': identity['user'],
                    'jobid': args['jobid'],
                    'filename': args['filename']
                   }, 404

