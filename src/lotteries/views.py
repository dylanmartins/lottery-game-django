from lotteries.models import LotteryGame, WinningBallot
from lotteries.serializers import LotteryGameSerializer, WinningBallotSerializer
from users.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from utilities.rest_framework import CreateReadViewset
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet


class LotteryAPI(CreateReadViewset):
    queryset = LotteryGame.objects.all()
    serializer_class = LotteryGameSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = LotteryGame.objects.filter(user=self.request.user)
        return queryset

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])


class WinningBallotAPI(ReadOnlyModelViewSet):
    queryset = WinningBallot.objects.all()
    serializer_class = WinningBallotSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
