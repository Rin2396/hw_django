"""Tests for forms."""
from django.test import TestCase

from main_game.forms import Join, Registration
from main_game.models import Club


class TestRegistrationForm(TestCase):
    """Test cases for the Registration form."""

    _valid_attrs = {
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'sirius@sirius.ru',
        'password1': 'Dayana2396000789',
        'password2': 'Dayana2396000789',
    }
    _not_nullable_fields = ('username', 'password1', 'password2')

    def test_empty(self):
        """Test the form with empty required fields."""
        for field in self._not_nullable_fields:
            attrs = self._valid_attrs.copy()
            attrs[field] = ''
            self.assertFalse(Registration(data=attrs).is_valid())

    def test_invalid_email(self):
        """Test the form with an invalid email format."""
        attrs = self._valid_attrs.copy()
        attrs['email'] = 'Dayana'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_different_password(self):
        """Test the form with different passwords."""
        attrs = self._valid_attrs.copy()
        attrs['password1'] = 'JHfdshkfdfkhs71239217'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_common_password(self):
        """Test the form with a common password."""
        attrs = self._valid_attrs.copy()
        attrs['password1'] = attrs['password2'] = 'Abcde123'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_numeric_password(self):
        """Test the form with a numeric password."""
        attrs = self._valid_attrs.copy()
        attrs['password1'] = attrs['password2'] = '123456789'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_short_password(self):
        """Test the form with a short password."""
        attrs = self._valid_attrs.copy()
        attrs['password1'] = attrs['password2'] = 'ABC123'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_successful(self):
        """Test the form with valid input."""
        self.assertTrue(Registration(data=self._valid_attrs).is_valid())


class TestJoinForm(TestCase):
    """Test cases for the Join form."""

    def setUp(self):
        """Set up the test environment."""
        # Create test data for clubs
        self.test_club = Club.objects.create(name='test club')

    def test_valid_form(self):
        """Test the form with valid club data."""
        form_data = {
            'club': self.test_club.id,
        }
        form = Join(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        """Test the form with empty data."""
        form = Join(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['club'], ['This field is required.'])

    def test_invalid_club(self):
        """Test the form with an invalid club ID."""
        form_data = {
            'club': 'invalid_id',
        }
        form = Join(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['club'], ['“invalid_id” is not a valid UUID.'])

    def test_no_club_selected(self):
        """Test the form without selecting a club."""
        form_data = {
            'club': '',
        }
        form = Join(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['club'], ['This field is required.'])
