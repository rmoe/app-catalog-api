from pecan import expose, redirect
from webob.exc import status_map


class RootController(object):

    @expose(generic=True, template='json')
    def index(self):
        return '{}'
