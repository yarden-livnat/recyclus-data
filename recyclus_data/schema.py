from webargs import fields

identity_args = {
    'user': fields.Str(required=True),
    'roles': fields.Str(required=True)
}


internal_store_args = {
    'user': fields.Str(required=True),
    'project': fields.Str(required=True),
    'jobid': fields.Str(required=True)
}


internal_delete_args = {
    'user': fields.Str(),
    'name': fields.Str(),
    'jobid': fields.Str()
}


store_args = {
    'identity': fields.Nested(identity_args),
    'user': fields.Str(required=True),
    'project': fields.Str(required=True),
    'jobid': fields.Str(required=True)
}

list_args = {
    'identity': fields.Nested(identity_args),
    'project': fields.Str(),
    'jobid': fields.Str()
}

fetch_args = {
    'identity': fields.Nested(identity_args),
    'jobid': fields.Str(equired=True),
    'filename': fields.Str(required=True)
}
