"""Tests for join."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client as DjangoTestClient
from main_game.models import Client, Club
from rest_framework import status

club_attrs = {'name': 'DEF', 'phone_number': '+79098087060'}

TEST_ID = 123


class JoinTest(TestCase):
    """Test cases for joining clubs."""

    _url = '/join/'
    api_client: DjangoTestClient
    client: Client
    user: User

    def setUp(self):
        """Set up the test environment."""
        self.user = User.objects.create(username='user', password='user')
        self.user.save()
        self.client = Client.objects.create(user=self.user)
        self.api_client = DjangoTestClient()
        self.api_client.force_login(self.user)

    def test_without_id(self):
        """Test joining without specifying a club ID."""
        self.assertEqual(self.api_client.post(self._url, {}).status_code, status.HTTP_302_FOUND)

    def test_invalid_id(self):
        """Test joining with an invalid club ID."""
        url = f'{self._url}?id=123'
        self.assertEqual(self.api_client.post(url, {}).status_code, status.HTTP_302_FOUND)

    def test_successful(self):
        """Test successful joining of a club."""
        club = Club.objects.create(**club_attrs)
        self.client.save()

        url = f'{self._url}?id={club.id}'
        self.api_client.post(url, {})
        self.client.refresh_from_db()

        self.assertIn(club, self.client.clubs.all())

    def test_repeated_join(self):
        """Test attempting to join the same club multiple times."""
        club = Club.objects.create(**club_attrs)
        self.client.save()

        url = f'{self._url}?id={club.id}'
        self.api_client.post(url, {})
        self.client.refresh_from_db()

        self.assertIn(club, self.client.clubs.all())

        self.api_client.post(url, {})
        self.client.refresh_from_db()

        self.assertEqual(len(self.client.clubs.filter(id=club.id)), 1)


class RemoveFromJoinedTest(TestCase):
    """Test cases for removing clubs from joined clubs."""

    _url_template = '/remove_from_joined/{club_id}/'
    api_client: DjangoTestClient
    client: Client
    user: User

    def setUp(self):
        """Set up the test environment."""
        self.user = User.objects.create(username='user', password='user')
        self.user.save()
        self.client = Client.objects.create(user=self.user)
        self.api_client = DjangoTestClient()
        self.api_client.force_login(self.user)

    def test_remove_valid_club(self):
        """Test removing a valid club from joined clubs."""
        club = Club.objects.create(**club_attrs)
        self.client.clubs.add(club)
        self.client.save()

        url = self._url_template.format(club_id=club.id)
        response = self.api_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.client.refresh_from_db()

        self.assertNotIn(club, self.client.clubs.all())

    def test_remove_invalid_club(self):
        """Test removing an invalid club ID from joined clubs."""
        url = self._url_template.format(club_id=TEST_ID)
        response = self.api_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_club_not_joined(self):
        """Test removing a club that the client has not joined."""
        club = Club.objects.create(**club_attrs)
        url = self._url_template.format(club_id=club.id)
        response = self.api_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.client.refresh_from_db()
        self.assertNotIn(club, self.client.clubs.all())
