# -*- coding: utf-8 -*-
from rest_framework.response import Response


class ListMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        object_list = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(object_list)

        if page is not None:
            serializer = self.get_pagination_serializer(page)

            return Response(
                serializer.data['results'],
                headers=self.get_pagination_headers(serializer)
            )

        else:
            serializer = self.get_serializer(object_list, many=True)

            return Response(serializer.data)

    def get_pagination_headers(self, serializer):
        """
        Return the link headers as described in RFC 5988 and a custom
        X-Total-Count header for representing the total available items.
        """
        headers = {'X-Total-Count': serializer.data['count']}

        if serializer.data['next']:
            template = '<{0}>; rel="next", '.format(serializer.data['next'])

        else:
            template = ''

        if serializer.data['last']:
            template = '{0}<{1}>; rel="last"'.format(
                template, serializer.data['last'])

        if template:
            headers.update(Link=template)

        return headers
