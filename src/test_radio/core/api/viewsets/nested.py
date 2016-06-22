from django.core.exceptions import ImproperlyConfigured

from rest_framework.generics import get_object_or_404

from store.core.api.viewsets import BaseApiViewset
from store.core.api.mixins import ListMixin, RetrieveMixin
from store.core.api.serializers.nested import NestedModelSerializer


class BaseNestedApiViewset(BaseApiViewset):
    """
    Simple view to handle nested resources.
    """
    parent_lookup_field = None
    parent_model = None
    parent_model_name = None
    parent_permission_classes = []
    parent_queryset = None
    _parent_object_cache = None

    def get_parent_permissions(self):
        """
        Instantiates and returns the list of parent permissions that this
        view requires.
        """
        return [permission() for permission in self.parent_permission_classes]

    def check_parent_object_permissions(self, request, obj):
        """
        Check if the request should be permitted for a given parent object.

        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_parent_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(request)

    def get_parent_queryset(self):
        """
        Get the list of parent items for this view.

        This must be an iterable, and may be a queryset.
        Defaults to using `self.parent_queryset`.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """
        if self.parent_queryset is not None:
            return self.parent_queryset._clone()

        if self.parent_model is not None:
            return self.parent_model._default_manager.all()

        raise ImproperlyConfigured("'%s' must define 'parent_queryset' or "
                                   "'parent_model'" % self.__class__.__name__)

    def get_parent_object(self, parent_queryset=None):
        """
        Returns the parent object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if parent objects are referenced using multiple
        keyword arguments in the url conf.
        """
        if self._parent_object_cache is not None:
            return self._parent_object_cache

        if parent_queryset is None:
            parent_queryset = self.get_parent_queryset()

        if self.parent_model is None:
            raise ImproperlyConfigured("'%s' must define 'parent_model'"
                                       % self.__class__.__name__)

        if self.parent_lookup_field is None:
            raise ImproperlyConfigured("'%s' must define 'parent_lookup_field'"
                                       % self.__class__.__name__)

        lookup_url_kwarg = '_'.join([
            self.parent_model_name or self.parent_model._meta.model_name,
            self.parent_lookup_field
        ])

        lookup = self.kwargs.get(lookup_url_kwarg, None)

        if lookup is not None:
            filter_kwargs = {self.parent_lookup_field: lookup}

        else:
            raise ImproperlyConfigured(
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the '
                '`parent_lookup_field` attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
            )

        obj = get_object_or_404(parent_queryset, **filter_kwargs)

        self.check_parent_object_permissions(self.request, obj)
        self._parent_object_cache = obj

        return obj

    def get_serializer(self, instance=None, data=None,
                       many=False, partial=False, klass=None):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = klass or None

        if not serializer_class:
            if self.action == 'create' and instance:
                serializer_class = getattr(
                    self, 'created_object_serializer_class',
                    getattr(self, 'retrieve_serializer_class', None)
                )

            else:
                serializer_class = self.get_serializer_class()

        if serializer_class is None:
            serializer_class = getattr(self, 'serializer_class')

        context = self.get_serializer_context()

        kwargs = {
            'data': data,
            'many': many,
            'partial': partial,
            'context': context,
        }

        if issubclass(serializer_class, NestedModelSerializer):
            kwargs.update(parent_object=self.get_parent_object())

        return serializer_class(instance, **kwargs)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        if issubclass(self.serializer_class, NestedModelSerializer):
            return {
                'request': self.request,
                'format': self.format_kwarg,
                'view': self,
                'parent_object': self.get_parent_object()
            }
        else:
            return {
                'request': self.request,
                'format': self.format_kwarg,
                'view': self,
            }


class NestedApiViewset(ListMixin, RetrieveMixin, BaseNestedApiViewset):
    """
    Simple view to handle nested resources.
    """
    pass
