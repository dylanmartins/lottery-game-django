from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from freezegun import freeze_time

from lotteries.models import LotteryGame, WinningBallot
from lotteries.tasks import get_todays_winning_game


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@freeze_time(datetime.today() + timedelta(days=1))
def test_get_todays_winning_game(valid_lottery_game):
    assert len(WinningBallot.objects.all()) == 0
    assert len(LotteryGame.objects.all()) == 1

    get_todays_winning_game()

    assert len(WinningBallot.objects.all()) == 1

    valid_lottery_game.refresh_from_db()
    assert valid_lottery_game.winning_game is True


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@freeze_time(datetime.today() + timedelta(days=1))
def test_get_todays_winning_game__multiple_numbers(valid_lottery_game, valid_lottery_game_b):
    assert len(WinningBallot.objects.all()) == 0
    assert len(LotteryGame.objects.all()) == 2
    assert valid_lottery_game.numbers == valid_lottery_game_b.numbers

    get_todays_winning_game()

    assert len(WinningBallot.objects.all()) == 1

    valid_lottery_game.refresh_from_db()
    valid_lottery_game_b.refresh_from_db()
    # We set only the first one created as winning_game True
    assert valid_lottery_game.winning_game is True
    assert valid_lottery_game_b.winning_game is False
    assert valid_lottery_game.created_at < valid_lottery_game_b.created_at


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@freeze_time(datetime.today() + timedelta(days=1))
@patch("lotteries.tasks.logger.info")
def test_get_todays_winning_game__should_not_sort_winning_games(logging_mock, valid_lottery_game):
    assert len(WinningBallot.objects.all()) == 0
    assert len(LotteryGame.objects.all()) == 1

    valid_lottery_game.winning_game = True
    valid_lottery_game.save()

    get_todays_winning_game()

    # We didn't create a new ballot because the only game was set as winning_game
    assert len(WinningBallot.objects.all()) == 0

    assert logging_mock.called
    assert logging_mock.call_args[0][0] == "There was no games today!"
