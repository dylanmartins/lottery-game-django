from __future__ import annotations

from rest_framework import mixins, viewsets


# I wanted a viewset where the user couldn't do PUT requests because
# it doesn't make sense to change a lottery game after you played.
# So, I created this "utilities" folder in case we want to make more customized stuff :)
class CreateReadViewset(
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass