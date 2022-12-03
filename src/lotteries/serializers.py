from lotteries.models import LotteryGame
from users.models import User
from rest_framework import serializers


class LotteryGameSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    numbers = serializers.ListField(required=True, child=serializers.IntegerField())

    class Meta:
        model = LotteryGame
        fields = "__all__"
        read_only_fields = ["uuid", "user", "winning_game", "created_at"]

    def validate_numbers(self, numbers):
        # We sort the numbers here to create a pattern,
        # this way it will be easier to filter by numbers in the future
        numbers.sort()
        return numbers
