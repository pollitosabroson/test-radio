# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json

from django.conf import settings
from django.utils import six

from rest_framework import renderers
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser

from store.core.utils.json import snakefy


class CamelCaseJSONParser(BaseParser):
    """
    Custom parser to transform a CamelCased JSON object to Python friendly
    snake_cased dictionary.
    """
    media_type = 'application/json'
    renderer_class = renderers.JSONRenderer

    def parse(self, stream, media_type=None, parser_context={}):
        """
        Parse the incoming bytestring as JSON and return the resulting
        data snake_cased.
        """
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            data = stream.read().decode(encoding)
            return snakefy(json.loads(data))

        except ValueError as e:
            raise ParseError('JSON parse error - %s' % six.text_type(e))
