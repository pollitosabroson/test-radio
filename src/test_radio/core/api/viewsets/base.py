from rest_framework import viewsets

from store.core.api.mixins import ListMixin, RetrieveMixin


class BaseApiViewset(viewsets.GenericViewSet):
    """
    Base viewset class that defines custom methods for get serializer
    depending on the viewset action method names.
    """
    def get_serializer_context(self):
        """
        Adds the current requesting user to the serializer context.
        """
        context = super(BaseApiViewset, self).get_serializer_context()

        if 'user' not in context and hasattr(self, 'request'):
            context.update(user=self.request.user)

        return context

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

        return serializer_class(
            instance,
            data=data,
            many=many,
            partial=partial,
            context=context
        )

    def get_queryset(self):
        """
        Set the queryset language if it is translatable and a language is
        provided in the request.
        """
        queryset = super(BaseApiViewset, self).get_queryset()
        orders = getattr(self, 'order_by', [])

        if isinstance(orders, str):
            orders = [orders]

        elif isinstance(orders, tuple):
            orders = list(orders)

        return queryset.order_by(*orders)


class ApiViewset(ListMixin, RetrieveMixin, BaseApiViewset):
    """
    Simple wieset with list and retrieve methods by default.
    """
    pass
