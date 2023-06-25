from rest_framework import filters, mixins, viewsets
from .permissions import (IsAdminOrReadOnlyPermission, )


class BaseViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'