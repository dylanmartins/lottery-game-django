import pytest
from lotteries.models import LOTTERY_GAME_SIZE, LotteryGame, WinningBallot
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


@pytest.fixture
def valid_winning_ballot(valid_lottery_game):
    payload = {
        "winning_games": [valid_lottery_game.pk]
    }
    return WinningBallot.objects.create(
        **payload
    )