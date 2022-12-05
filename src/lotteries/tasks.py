import logging
from datetime import date, datetime, timedelta

from celery import shared_task
from django.db import transaction
from django.db.utils import IntegrityError

from lotteries.models import LotteryGame, WinningBallot


logger = logging.getLogger(__name__)


@shared_task
def get_todays_winning_game():

    logger.info(f"Starting task get_todays_winning_game now {datetime.now()}")

    # Since this task executes after midnight we need to get the day before
    todays_date = date.today()
    yesterday = todays_date - timedelta(days=1)

    logger.info(f"Getting all lottery games from {yesterday}")

    todays_lottery_games = LotteryGame.objects.filter(game_date=yesterday, winning_game=False)
    if not todays_lottery_games:
        logger.info("There was no games today!")
        return

    # We sort a random winner
    random_winner = todays_lottery_games.order_by("?").first()

    # We check if there are more games with the same numbers
    games_with_same_number = todays_lottery_games.filter(numbers=random_winner.numbers).order_by("created_at")
    if games_with_same_number.count() > 1:
        logger.info("Found more games with the same numbers!")
        # it means there are more games with the same numbers so we get the first one created
        random_winner = games_with_same_number.first()

    logger.info(f"The user {random_winner.pk} won todays lottery game with the game {random_winner.pk}")

    try:
        with transaction.atomic():
            # TODO: in the future if we plan to allow more winners we just need
            # to add the list of games with the same numbers
            payload = {"winning_games": [random_winner.pk]}
            winning_ballot = WinningBallot(**payload)
            winning_ballot.save()

            random_winner.winning_game = True
            random_winner.save()
    except IntegrityError as exc:
        # Some error ocurred when trying to save the winning
        # ballot or the winning game
        logger.info(f"Finished task get_todays_winning_game with errors: {exc}")
        return

    logger.info("Finished task get_todays_winning_game succesfully")
