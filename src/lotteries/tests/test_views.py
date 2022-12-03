from lotteries.models import LOTTERY_GAME_SIZE, LotteryGame
from django.urls import reverse

import pytest


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_lottery_game_api__success(auth_api_client, valid_create_lottery_payload, valid_user):

    assert len(LotteryGame.objects.filter(user=valid_user)) == 0

    response = auth_api_client.post(reverse("lotteries:lottery-list"), data=valid_create_lottery_payload)
    assert response.status_code == 201

    assert len(LotteryGame.objects.filter(user=valid_user)) == 1


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

    assert len(LotteryGame.objects.filter(user=valid_user)) == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_detail_lottery_games_api__success(auth_api_client, valid_user, valid_lottery_game):

    assert len(LotteryGame.objects.filter(user=valid_user)) == 1

    response = auth_api_client.get(reverse("lotteries:lottery-detail", kwargs={"pk": valid_lottery_game.pk}))
    assert response.status_code == 200
    assert response.data["uuid"] == str(valid_lottery_game.pk)
    assert response.data["numbers"] == list(range(LOTTERY_GAME_SIZE))
    assert response.data["winning_game"] == False
    assert str(response.data["user"]) == str(valid_user.pk)
