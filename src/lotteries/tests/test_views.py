from datetime import date, timedelta

import pytest
from django.urls import reverse

from lotteries.models import LOTTERY_GAME_SIZE, LotteryGame, WinningBallot


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_lottery_game_api__success(auth_api_client, valid_create_lottery_payload, valid_user):

    assert len(LotteryGame.objects.filter(user=valid_user)) == 0

    response = auth_api_client.post(reverse("lotteries:lottery-list"), data=valid_create_lottery_payload)
    assert response.status_code == 201

    assert len(LotteryGame.objects.filter(user=valid_user)) == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_lottery_game_api__for_specific_date(auth_api_client, valid_create_lottery_payload, valid_user):

    assert len(LotteryGame.objects.filter(user=valid_user)) == 0

    tomorrow = date.today() + timedelta(days=1)
    valid_create_lottery_payload["game_date"] = tomorrow.strftime("%Y-%m-%d")

    response = auth_api_client.post(reverse("lotteries:lottery-list"), data=valid_create_lottery_payload)
    assert response.status_code == 201

    lottery_game = LotteryGame.objects.get(pk=response.data["uuid"])
    assert lottery_game.game_date == tomorrow


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_lottery_game_api__fails_trying_to_play_past_games(
    auth_api_client, valid_create_lottery_payload, valid_user
):

    assert len(LotteryGame.objects.filter(user=valid_user)) == 0

    # Trying to create a game for past ballots
    two_days_ago = date.today() - timedelta(days=2)
    valid_create_lottery_payload["game_date"] = two_days_ago.strftime("%Y-%m-%d")

    response = auth_api_client.post(reverse("lotteries:lottery-list"), data=valid_create_lottery_payload)
    assert response.status_code == 400
    assert str(response.data["game_date"][0]) == "You can't play past lottery games!"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_lottery_game_api__fails_unauthorized_request(api_client, valid_create_lottery_payload, valid_user):

    assert len(LotteryGame.objects.filter(user=valid_user)) == 0

    response = api_client.post(reverse("lotteries:lottery-list"), data=valid_create_lottery_payload)
    assert response.status_code == 403

    assert len(LotteryGame.objects.filter(user=valid_user)) == 0


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_lottery_games_api__success(auth_api_client, valid_user, valid_lottery_game):

    assert len(LotteryGame.objects.filter(user=valid_user)) == 1

    response = auth_api_client.get(reverse("lotteries:lottery-list"))
    assert response.status_code == 200

    lottery_game = response.data[0]
    assert lottery_game["uuid"] == str(valid_lottery_game.pk)
    assert lottery_game["numbers"] == list(range(LOTTERY_GAME_SIZE))
    assert lottery_game["winning_game"] is False
    assert lottery_game["game_date"] == date.today().strftime("%Y-%m-%d")
    assert str(lottery_game["user"]) == str(valid_user.pk)


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_detail_lottery_games_api__success(auth_api_client, valid_user, valid_lottery_game):

    assert len(LotteryGame.objects.filter(user=valid_user)) == 1

    response = auth_api_client.get(reverse("lotteries:lottery-detail", kwargs={"pk": valid_lottery_game.pk}))
    assert response.status_code == 200
    assert response.data["uuid"] == str(valid_lottery_game.pk)
    assert response.data["numbers"] == list(range(LOTTERY_GAME_SIZE))
    assert response.data["winning_game"] is False
    assert str(response.data["user"]) == str(valid_user.pk)


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_detail_lottery_games_api__fails_not_found(auth_api_client, valid_user, valid_lottery_game):

    assert len(LotteryGame.objects.filter(user=valid_user)) == 1

    response = auth_api_client.get(reverse("lotteries:lottery-detail", kwargs={"pk": "invalid_pk"}))
    assert response.status_code == 404


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_lottery_game_api__numbers_are_sorted_when_creating(
    auth_api_client, valid_create_lottery_payload, valid_user
):

    assert len(LotteryGame.objects.filter(user=valid_user)) == 0

    valid_create_lottery_payload["numbers"] = [66, 12, 1, 102, 0]
    response = auth_api_client.post(reverse("lotteries:lottery-list"), data=valid_create_lottery_payload)
    assert response.status_code == 201
    assert response.data["numbers"] == [0, 1, 12, 66, 102]


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_lottery_game_api__setting_winning_game_as_true(
    auth_api_client, valid_create_lottery_payload, valid_user
):

    assert len(LotteryGame.objects.filter(user=valid_user)) == 0

    valid_create_lottery_payload["winning_game"] = True
    response = auth_api_client.post(reverse("lotteries:lottery-list"), data=valid_create_lottery_payload)
    assert response.status_code == 201
    # it's still False because this field is read only
    assert response.data["winning_game"] is False


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_lottery_games_api__check_winning_game(auth_api_client, valid_user, valid_lottery_game):

    valid_lottery_game.winning_game = True
    valid_lottery_game.save()

    response = auth_api_client.get(reverse("lotteries:lottery-list"))
    assert response.status_code == 200

    lottery_game = response.data[0]
    assert lottery_game["uuid"] == str(valid_lottery_game.pk)
    assert lottery_game["numbers"] == list(range(LOTTERY_GAME_SIZE))
    # Set as True
    assert lottery_game["winning_game"] is True
    assert str(lottery_game["user"]) == str(valid_user.pk)


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_winning_ballots_api__success(auth_api_client, valid_user, valid_lottery_game, valid_winning_ballot):

    assert len(WinningBallot.objects.all()) == 1

    response = auth_api_client.get(reverse("lotteries:winning_ballot-list"))
    assert response.status_code == 200

    lottery_game = response.data[0]
    assert lottery_game["uuid"] == str(valid_winning_ballot.pk)
    assert lottery_game["winning_games"] == [str(valid_lottery_game.pk)]
    assert lottery_game["winning_users"] == [f"{valid_user.first_name} {valid_user.last_name}"]
    assert lottery_game["winning_numbers"] == valid_lottery_game.numbers


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_winning_ballots_api__fails_when_there_is_no_winnings_games(
    auth_api_client,
):

    assert len(WinningBallot.objects.all()) == 0

    response = auth_api_client.get(reverse("lotteries:winning_ballot-list"))
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_detail_winning_ballots_api__success(auth_api_client, valid_lottery_game, valid_winning_ballot):

    assert len(WinningBallot.objects.all()) == 1

    response = auth_api_client.get(reverse("lotteries:winning_ballot-detail", kwargs={"pk": valid_winning_ballot.pk}))
    assert response.status_code == 200

    lottery_game = response.data
    assert lottery_game["uuid"] == str(valid_winning_ballot.pk)
    assert lottery_game["winning_games"] == [str(valid_lottery_game.pk)]
