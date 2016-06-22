# -*- coding: utf-8 -*-
from rest_framework.mixins import CreateModelMixin
from rest_framework.settings import api_settings


class CreateMixin(CreateModelMixin):
    """
    Create a model instance.
    """
    url_field_name = None

    def get_success_headers(self, data):
        headers = {}

        if self.url_field_name is not None:
            location = data.get(self.url_field_name, None)

            if location:
                headers.update({'Location': location})

        else:
            try:
                return {'Location': data[api_settings.URL_FIELD_NAME]}

            except (TypeError, KeyError):
                return {}
