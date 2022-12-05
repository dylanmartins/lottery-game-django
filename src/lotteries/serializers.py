from __future__ import annotations

from datetime import date

from rest_framework import exceptions, serializers

from lotteries.models import LOTTERY_GAME_SIZE, LotteryGame, WinningBallot
from users.models import User


class LotteryGameSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    # NOTE: We could check for duplicate items inside `numbers`,
    # but this is a small detail so I'll leave it open
    numbers = serializers.ListField(
        required=True,
        child=serializers.IntegerField(),
        max_length=LOTTERY_GAME_SIZE,
        min_length=LOTTERY_GAME_SIZE,
    )
    game_date = serializers.DateField(required=False)

    class Meta:
        model = LotteryGame
        fields = "__all__"
        read_only_fields = ["uuid", "user", "winning_game", "game_date", "created_at"]

    def validate(self, data: dict) -> dict:
        validated_data = super().validate(data)

        # We sort the numbers here to create a pattern,
        # this way it will be easier to filter by numbers in the future
        validated_data["numbers"].sort()

        if validated_data.get("game_date") and validated_data.get("game_date") < date.today():
            raise exceptions.ValidationError({"game_date": "You can't play past lottery games!"})

        return validated_data


class WinningBallotSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinningBallot
        fields = ["uuid", "winning_games", "winning_numbers", "winning_users", "created_at"]


class UrlParamSerializer(serializers.Serializer):
    from_date = serializers.DateTimeField(required=False)
    to_date = serializers.DateTimeField(required=False)
