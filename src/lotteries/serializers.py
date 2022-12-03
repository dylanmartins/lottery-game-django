from __future__ import annotations

from rest_framework import serializers

from lotteries.models import LOTTERY_GAME_SIZE, LotteryGame, WinningBallot
from users.models import User


class LotteryGameSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        required=True, queryset=User.objects.all()
    )
    # NOTE: We could check for duplicate items inside `numbers`,
    # but this is a small detail so I'll leave it open
    numbers = serializers.ListField(
        required=True,
        child=serializers.IntegerField(),
        max_length=LOTTERY_GAME_SIZE,
        min_length=LOTTERY_GAME_SIZE,
    )

    class Meta:
        model = LotteryGame
        fields = "__all__"
        read_only_fields = ["uuid", "user", "winning_game", "created_at"]

    def validate_numbers(self, numbers: list[int]) -> list[int]:
        # We sort the numbers here to create a pattern,
        # this way it will be easier to filter by numbers in the future
        numbers.sort()
        return numbers


class WinningBallotSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinningBallot
        fields = "__all__"
