from __future__ import annotations

from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from lotteries.models import LotteryGame, WinningBallot
from lotteries.serializers import LotteryGameSerializer, UrlParamSerializer, WinningBallotSerializer
from users.authentication import JWTAuthentication
from utilities.rest_framework import CreateReadViewset


class LotteryAPI(CreateReadViewset):
    queryset = LotteryGame.objects.all()
    serializer_class = LotteryGameSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[LotteryGame]:
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            return LotteryGame.objects.none()

        queryset = LotteryGame.objects.filter(user=self.request.user)
        query_params = self.request.GET.dict()

        # Validate filters
        serializer = UrlParamSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)

        from_date = serializer.validated_data.get("from_date", None)
        if from_date:
            queryset = queryset.filter(created_at__gte=from_date)

        to_date = serializer.validated_data.get("to_date", None)
        if to_date:
            queryset = queryset.filter(created_at__lte=to_date)

        return queryset

    @swagger_auto_schema(query_serializer=UrlParamSerializer)
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])


class WinningBallotAPI(ReadOnlyModelViewSet):
    queryset = WinningBallot.objects.all()
    serializer_class = WinningBallotSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[WinningBallot]:
        queryset = WinningBallot.objects.all().order_by("-created_at")
        query_params = self.request.GET.dict()

        # Validate filters
        serializer = UrlParamSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)

        from_date = serializer.validated_data.get("from_date", None)
        if from_date:
            queryset = queryset.filter(created_at__gte=from_date)

        to_date = serializer.validated_data.get("to_date", None)
        if to_date:
            queryset = queryset.filter(created_at__lte=to_date)

        return queryset

    @swagger_auto_schema(query_serializer=UrlParamSerializer)
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
