from django.core.exceptions import ImproperlyConfigured

from rest_framework.reverse import reverse

from .base import ModelSerializer

DEFAULT_ERROR_MESSAGES = {
    'required': 'required',
    'invalid': 'invalid',
    'invalid_choice': 'invalid',
    'min_length': 'minlength',
    'max_length': 'maxlength'
}


class ParentObjectMixin(object):
    """
    Simple mixin to extends a serializer __init__ method to allow an optional
    parenrt_object parameter. Useful for nested serializers whose need to
    access a parent resource.
    """
    def __init__(self, *args, **kwargs):
        self.parent_object = kwargs.pop('parent_object', None)

        super(ParentObjectMixin, self).__init__(*args, **kwargs)


class NestedModelSerializer(ParentObjectMixin, ModelSerializer):
    """
    Simple serializer for nested model objects.
    """
    parent_name = None
    parent_lookup_field = None

    def get_resource_uri(self, obj):
        """
        Return the uri of the given nested object.
        """
        if self.parent_name is None:
            raise ImproperlyConfigured("'%s' must define 'parent_name'"
                                       % self.__class__.__name__)

        if self.parent_lookup_field is None:
            raise ImproperlyConfigured("'%s' must define 'parent_lookup_field'"
                                       % self.__class__.__name__)

        url = 'store:api:%s-detail' % getattr(
            self, 'resource_view_name',
            self.Meta.model._meta.object_name.lower()
        )

        try:
            parent = getattr(obj, self.parent_name, None)
            parent_lookup = '_'.join((self.parent_name,
                                      self.parent_lookup_field))

        except:
            return None

        return reverse(url, request=self.context.get('request', None), kwargs={
            parent_lookup: getattr(parent, self.parent_lookup_field),
            self.lookup_field: getattr(obj, self.lookup_field)
        })
