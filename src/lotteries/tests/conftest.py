import pytest
from lotteries.models import LOTTERY_GAME_SIZE, LotteryGame
import copy


@pytest.fixture
def valid_create_lottery_payload(valid_user):
    return {
        "user": valid_user.pk,
        "numbers": list(range(LOTTERY_GAME_SIZE)),
    }


@pytest.fixture
def valid_lottery_game(valid_user, valid_create_lottery_payload):
    payload = copy.copy(valid_create_lottery_payload)
    payload["user"] = valid_user
    return LotteryGame.objects.create(
        **payload
    )
