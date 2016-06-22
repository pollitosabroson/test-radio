# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json

from django.http.multipartparser import parse_header
from django.utils import six

from rest_framework.renderers import BaseRenderer
from rest_framework.utils import encoders

from store.core.utils.json import camelfy


class CamelCaseJSONRenderer(BaseRenderer):
    """
    Custom renderer to transform a Python snake_cased object to a JSON
    CamelCased bytestring.
    """
    media_type = 'application/json'
    format = 'json'
    encoder_class = encoders.JSONEncoder
    ensure_ascii = True

    # We don't set a charset because JSON is a binary encoding,
    # that can be encoded as utf-8, utf-16 or utf-32.
    charset = None

    def get_indent(self, accepted_media_type, renderer_context):
        if accepted_media_type:
            # If the media type looks like 'application/json; indent=4',
            # then pretty print the result.
            base_media_type, params = parse_header(
                accepted_media_type.encode('ascii'))

            try:
                return max(min(int(params['indent']), 8), 0)

            except (KeyError, ValueError, TypeError):
                pass

        # If 'indent' is provided in the context, then pretty print the result.
        # E.g. If we're being called by the BrowsableAPIRenderer.
        return renderer_context.get('indent', None)

    def render(self, data, accepted_media_type=None, renderer_context={}):
        """
        Render `data` into CamelCased JSON, returning a bytestring.
        """
        if data is None:
            return bytes()

        indent = self.get_indent(accepted_media_type, renderer_context)

        camel_cased_data = camelfy(data)

        ret = json.dumps(
            camel_cased_data,
            cls=self.encoder_class,
            indent=indent,
            ensure_ascii=self.ensure_ascii
        )

        # On python 2.x json.dumps() returns bytestrings if ensure_ascii=True,
        # but if ensure_ascii=False, the return type is underspecified,
        # and may (or may not) be unicode.
        # On python 3.x json.dumps() returns unicode strings.
        if isinstance(ret, six.text_type):
            return bytes(ret.encode('utf-8'))

        return ret
