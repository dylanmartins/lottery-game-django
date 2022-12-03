from lotteries.models import LotteryGame
from rest_framework import serializers


class LotteryGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = LotteryGame
        fields = "__all__"