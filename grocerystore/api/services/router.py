from typing import NamedTuple

from rest_framework.viewsets import ViewSet


class RouterRegisterParams(NamedTuple):
    prefix: str
    viewset: ViewSet
    basename: str
