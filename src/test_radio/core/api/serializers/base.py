from collections import OrderedDict

from rest_framework import serializers
from rest_framework.reverse import reverse


class AbsoluteUriMixin(object):
    """
    Simple mixin that brings a method for returning a fully qualified
    absolute uri.
    """
    def build_absolute_uri(self, uri):
        """
        Return a fully qualified absolute url for the given uri.
        """
        request = self.context.get('request', None)

        return (request.build_absolute_uri(uri) if
                request is not None else uri)


class DynamicFieldsMixin(object):
    """
    Simple mixin that allows a serializer to be initialized specifying the
    fields to be serialized.

    Example:

        class MySerializer(serializers.ModelSerializer):
            class Meta:
                model = MyModel
                fields = ['field1', 'field2', ..., 'fieldN']

        serializer = Myserializer(instance, fields=['field1', 'field3'])

        print serializer.data
        >>> {'field1': 'some data', 'field3': 'another data'}
    """
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsMixin, self).__init__(*args, **kwargs)

        if fields is not None:
            self.fields = OrderedDict([
                (f, self.fields.get(f)) for f in fields if f in self.fields
            ])


class ParentObjectMixin(object):
    """
    Simple mixin to extends a serializer __init__ method to allow an optional
    parenrt_object parameter. Useful for nested serializers whose need to
    access a parent resource.
    """
    def __init__(self, *args, **kwargs):
        self.parent_object = kwargs.pop('parent_object', None)

        super(ParentObjectMixin, self).__init__(*args, **kwargs)


class ModelSerializer(DynamicFieldsMixin, AbsoluteUriMixin,
                      serializers.ModelSerializer):
    """
    Simple serializer for model objects.
    """
    lookup_field = 'public_id'

    id = serializers.CharField(
        source='public_id',
        read_only=True
    )
    resource_uri = serializers.SerializerMethodField()

    def get_resource_uri(self, obj):
        """
        Return the uri of the given object.
        """
        url = 'store:api:%s-detail' % getattr(
            self, 'resource_view_name',
            self.Meta.model._meta.model_name
        )

        return reverse(url, request=self.context.get('request', None), kwargs={
            self.lookup_field: getattr(obj, self.lookup_field)
        })
