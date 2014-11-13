import factory
from django.contrib.auth.models import User
from teachrecovery.main.models import CoinGame, GameSubmission


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: "user%03d" % n)
    is_staff = True


class CoinGameFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CoinGame


class GameSubmissionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = GameSubmission
    user = factory.SubFactory(UserFactory)
    game = factory.SubFactory(CoinGameFactory)
