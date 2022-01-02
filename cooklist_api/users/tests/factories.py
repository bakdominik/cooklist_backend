import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):

    password = "Password123"
    username = factory.Sequence(lambda n: "user_%s" % n)
    first_name = factory.Sequence(lambda n: "first_name_%s" % n)
    last_name = factory.Sequence(lambda n: "last_name_%s" % n)
    email = factory.Sequence(lambda n: "user_%s@i2a.test" % n)

    class Meta:
        model = User
