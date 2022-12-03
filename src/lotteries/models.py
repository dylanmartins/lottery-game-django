import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from users.models import User

LOTTERY_GAME_SIZE = 5


class LotteryGame(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(
        User, related_name="lottery_games", on_delete=models.CASCADE
    )
    numbers = ArrayField(
        models.IntegerField(db_index=True), size=LOTTERY_GAME_SIZE, default=list
    )
    created_at = models.DateTimeField(auto_now_add=True)
    winning_game = models.BooleanField(default=False)


class WinningBallot(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    winning_games = ArrayField(
        models.UUIDField(editable=False, unique=True), default=list
    )
    created_at = models.DateTimeField(auto_now_add=True)
