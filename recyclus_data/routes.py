from flask import Blueprint, current_app as app, request
from flask_restplus import Api, Resource
from webargs.flaskparser import use_args
from pathlib import Path

from .schema import store_args, internal_store_args
from .datastore import datastore
blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Recyclus data service',
          version='1.0',
          description='Remote cyclus data services api',
          doc='/doc/')


@api.route('/internal/store')
class Store(Resource):
    @use_args(internal_store_args)
    def post(self, args):
        path = Path('/repository') / args['jobid']
        path.mkdir(parents=True, exist_ok=True)
        for name, f in request.files.items():
            app.logger.debug('fields: %s: %s ', name, f.filename)
            f.save(str(path / f.filename))
        datastore.db.files.insert_one({
            'user': args['user'],
            'jobid': args['jobid'],
            'files': request.files.keys()
        })


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


@api.route('/fetch/<jobid>')
class Fetch(Resource):

    # @use_kwargs(CancelSchema())
    def get(self):
        return 'ok'



