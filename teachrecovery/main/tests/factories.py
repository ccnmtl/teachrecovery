import factory
from django.contrib.auth.models import User
from teachrecovery.main.models import CoinGame, GameSubmission


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user%03d" % n)
    is_staff = True


class CoinGameFactory(factory.DjangoModelFactory):
    class Meta:
        model = CoinGame


class GameSubmissionFactory(factory.DjangoModelFactory):
    class Meta:
        model = GameSubmission
    user = factory.SubFactory(UserFactory)
    game = factory.SubFactory(CoinGameFactory)
