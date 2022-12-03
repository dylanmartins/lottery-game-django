from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from users.authentication import JWTAuthentication
from users.serializers import UserSerializer
from users.models import User
 

class UsersAPIView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self, uuid):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, uuid=uuid)

    def register(self, request):
        data = request.data

        if data.get("password") != data.get("confirm_password"):
            raise exceptions.APIException("Passwords do not match")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Generate and return a token to be used right away.
        user = self.get_object(serializer.data.get("uuid"))
        token = user.generate_access_token()
        data = serializer.data
        # We do this to facilitate the usability, this way the user
        # don't need to do more than one request when login
        # for the first time
        data["access_token"] = f"Bearer {token}"
        return Response(data, status=status.HTTP_201_CREATED)

    def get_token(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise exceptions.AuthenticationFailed("Login error")

        response = Response(status=status.HTTP_200_OK)
        token = user.generate_access_token()
        response.data = {
            "access_token": f"Bearer {token}"
        }
        return response


class AuthenticatedUsersAPIView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, uuid=pk)

    def retrieve(self, request):
        obj = self.get_object(request.user.pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object(request.user.pk)
        # NOTE: We could implement here a soft_delete in case the user wants to come back
        # and keep the same lottery games, but then we would need to think about "what if another
        # person tries to create an user with the same data, how we will now that it's the same person
        obj.delete()
        return Response({"message": "Delete requested successfully"}, status=status.HTTP_202_ACCEPTED)
