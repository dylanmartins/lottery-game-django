from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
from users.serializers import UserSerializer
from users.models import User
 

class UsersAPIView(GenericViewSet, OAuthLibMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def sign_in(self, request):
        data = request.data

        if data.get('password') != data.get('password_confirm'):
            raise exceptions.APIException('Passwords do not match')

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def test(self, request):
        return Response({'test': True}, status=status.HTTP_201_CREATED)
