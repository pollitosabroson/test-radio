# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework import pagination
from rest_framework.templatetags.rest_framework import replace_query_param


class LastPageField(serializers.Field):
    """
    Field that returns a link to the last page in paginated results.
    """
    page_field = 'page'

    def to_representation(self, value):
        if not value.has_next():
            return None

        page = value.paginator._get_num_pages()
        request = self.context.get('request')
        url = request and request.build_absolute_uri() or ''

        return replace_query_param(url, self.page_field, page)


class PaginationSerializer(pagination.BasePaginationSerializer):
    """
    Custom pagination serializer implementing next and last links.
    """
    count = serializers.ReadOnlyField(source='paginator.count')
    next = pagination.NextPageField(source='*')
    last = LastPageField(source='*')
