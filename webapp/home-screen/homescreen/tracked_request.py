from uuid import uuid4

from pyramid.request import Request
from pyramid.decorator import reify


class TrackedRequest(Request):
    @reify
    def id(self):
        return str(uuid4())

