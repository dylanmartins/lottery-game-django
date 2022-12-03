from lotteries.models import LotteryGame
from lotteries.serializers import LotteryGameSerializer
from users.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from utilities.rest_framework import CreateReadViewset
from rest_framework.generics import get_object_or_404


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
