from rest_framework.routers import SimpleRouter

from lotteries import views


router = SimpleRouter()
router.trailing_slash = "/?"
router.register("lotteries", views.LotteryAPI, basename="lottery")
router.register("winning_ballots", views.WinningBallotAPI, basename="winning_ballot")

app_name = "lotteries"
urlpatterns = router.urls
