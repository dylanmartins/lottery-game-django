from __future__ import annotations

import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from users.models import User


LOTTERY_GAME_SIZE = 5


class LotteryGame(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, related_name="lottery_games", on_delete=models.CASCADE)
    numbers = ArrayField(models.IntegerField(db_index=True), size=LOTTERY_GAME_SIZE, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    winning_game = models.BooleanField(default=False)


class WinningBallot(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    winning_games = ArrayField(models.UUIDField(editable=False, unique=True), default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def winning_numbers(self) -> list[int] | None:
        if not self.winning_games:
            return None

        winning_game = LotteryGame.objects.get(pk=self.winning_games[0])
        return winning_game.numbers

    @property
    def winning_users(self) -> list[str] | None:
        if not self.winning_games:
            return None

        lottery_game_pks = [str(pk) for pk in self.winning_games]
        winning_games = LotteryGame.objects.filter(pk__in=lottery_game_pks)
        return [f"{game.user.first_name} {game.user.last_name}" for game in winning_games]
