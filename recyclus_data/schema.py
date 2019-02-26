from webargs import fields

identity_args = {
    'user': fields.Str(required=True),
    'roles': fields.Str(required=True)
}

internal_store_args = {
    'user': fields.Str(required=True),
    'name': fields.Str(required=True),
    'jobid': fields.Str(required=True)
}


store_args = {
    'identity': fields.Nested(identity_args),
    'user': fields.Str(required=True),
    'name': fields.Str(required=True),
    'jobid': fields.Str(required=True)
}
