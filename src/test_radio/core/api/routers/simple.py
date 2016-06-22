# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter as BaseRouter
from rest_framework.routers import Route, DynamicDetailRoute, DynamicListRoute


class SimpleRouter(BaseRouter):
    """
    Custom Router that maps viewset methods to its methodnamehyphen variant.

    For example:
        Method do_some_stuff will be translated to url resource/do-some-stuff
    """
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        DynamicListRoute(
            url=r'^{prefix}/{methodnamehyphen}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicDetailRoute(
            url=r'^{prefix}/{lookup}/{methodnamehyphen}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]
