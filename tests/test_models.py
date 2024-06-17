"""Tests for models."""

from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from main_game import models

valid_attrs = {
    'club': {'name': 'ABC', 'phone_number': 'ABC'},
    'boardgame': {'name': 'ABC', 'level': '99'},
    'genre': {'name': 'ABC', 'description': 'ABC'},
    'address': {'region': 'ABC', 'city': 'ABC', 'street': 'ABC', 'home': 'ABC'},
    'gameset': {'name': 'ABC', 'description': 'ABC'},
}

TEST_DATE1 = 2007
TEST_DATE2 = 3000


def create_model_tests(model_class, creation_attrs):
    """Create test case for successful creation of a model instance.

    Args:
        model_class (class): Model class to test.
        creation_attrs (dict): Attributes to use for creating the model instance.

    Returns:
        class: Test case class for the model.
    """
    class ModelTest(TestCase):
        def test_successful_creation(self):
            """Test successful creation of the model instance."""
            model_class.objects.create(**creation_attrs)
    return ModelTest


ClubModelTest = create_model_tests(models.Club,  valid_attrs.get('club'))
BoardGameModelTest = create_model_tests(models.BoardGame,  valid_attrs.get('boardgame'))
GenreModelTest = create_model_tests(models.Genre, valid_attrs.get('genre'))
AddressModelTest = create_model_tests(models.Address, valid_attrs.get('address'))
GameSetModelTest = create_model_tests(models.GameSet,  valid_attrs.get('gameset'))


class TestLinks(TestCase):
    """Test cases for model relationships."""

    def test_clubgame(self):
        """Test linking a board game to a club."""
        game = models.BoardGame.objects.create(**valid_attrs.get('boardgame'))
        club = models.Club.objects.create(**valid_attrs.get('club'))
        club.games.add(game)
        club.save()
        clubgame_link = models.ClubToGame.objects.filter(club=club, game=game)
        self.assertEqual(len(clubgame_link), 1)

    def test_clubaddress(self):
        """Test linking an address to a club."""
        club = models.Club.objects.create(**valid_attrs.get('club'))
        address = models.Address.objects.create(**valid_attrs.get('address'))
        club.addresses.add(address)
        club.save()
        clubaddress_link = models.ClubAddress.objects.filter(club=club, address=address)
        self.assertEqual(len(clubaddress_link), 1)

    def test_clubclient(self):
        """Test linking a client to a club."""
        user = User.objects.create(username='user', password='user')
        client = models.Client.objects.create(user=user)
        club = models.Club.objects.create(**valid_attrs.get('club'))
        client.clubs.add(club)
        client.save()
        clubclient_link = models.ClubClient.objects.filter(club=club, client=client)
        self.assertEqual(len(clubclient_link), 1)


valid_tests = (
    (models.check_created, datetime(TEST_DATE1, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_modified, datetime(TEST_DATE1, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_level, 30),
    (models.phone_number_validator, '+79098087060'),
)
invalid_tests = (
    (models.check_created, datetime(TEST_DATE2, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_modified, datetime(TEST_DATE2, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_level, 3000),
    (models.check_level, -3),
    (models.phone_number_validator, '+7909ee8087060'),
    (models.phone_number_validator, '+790980870600'),
    (models.phone_number_validator, '79098087060'),
)


def create_validation_test(validator, value, valid=True):
    """Create a validation test function.

    Args:
        validator (function): Validator function to test.
        value (Any): Value to test with the validator.
        valid (bool, optional): Whether the value is expected to be valid. Defaults to True.

    Returns:
        function: Validation test function.
    """
    def test(self):
        """Validation test function.

        Args:
            self (class): self
        """
        with self.assertRaises(ValidationError):
            validator(value)
    return lambda _: validator(value) if valid else test


invalid_methods = {
    f'test_invalid_{args[0].__name__}': create_validation_test(*args, valid=False) for args in invalid_tests
}
valid_methods = {
    f'test_valid_{args[0].__name__}': create_validation_test(*args) for args in valid_tests
}
TestValidators = type('TestValidators', (TestCase,), invalid_methods | valid_methods)
