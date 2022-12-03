from __future__ import annotations

from rest_framework import exceptions, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.authentication import JWTAuthentication
from users.models import User
from users.serializers import UserSerializer, UserTokenSerializer


class UsersRegisterAPIView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self, pk: str) -> User:
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=pk)

    def register(self, request: Request) -> Response:
        data = request.data

        if data.get("password") != data.get("confirm_password"):
            raise exceptions.APIException("Passwords do not match")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Generate and return a token to be used right away.
        user: User = self.get_object(serializer.data.get("uuid"))
        token: str = user.generate_access_token()
        data = serializer.data
        # We do this to facilitate the usability, this way the user
        # don't need to do more than one request when login
        # for the first time
        data["access_token"] = f"Bearer {token}"
        return Response(data, status=status.HTTP_201_CREATED)


class UsersTokenAPIView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserTokenSerializer

    def get_token(self, request: Request) -> Response:
        email = request.data.get("email")
        password = request.data.get("password")
        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise exceptions.AuthenticationFailed("Login error")

        token: str = user.generate_access_token()
        return Response({"access_token": f"Bearer {token}"}, status=status.HTTP_200_OK)


class AuthenticatedUsersAPIView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk: str) -> User:
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=pk)

    def retrieve(self, request: Request) -> Response:
        obj: User = self.get_object(request.user.pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        obj = self.get_object(request.user.pk)
        # NOTE: We could implement here a soft_delete in case the user wants to come back
        # and keep the same lottery games, but then we would need to think about "what if another
        # person tries to create an user with the same data, how we will now that it's the same person
        obj.delete()
        return Response(
            {"message": "Delete requested successfully"},
            status=status.HTTP_202_ACCEPTED,
        )
