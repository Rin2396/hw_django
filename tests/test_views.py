"""Tests for views."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from rest_framework import status

from main_game import models


def create_successful_page_test(page_url, page_name, template, auth=True):
    """Create a test function for successful page access.

    Args:
        page_url (str): URL of the page to test.
        page_name (str): Name of the page.
        template (str): Expected template used for rendering.
        auth (bool, optional): Whether to authenticate the user. Defaults to True.

    Returns:
        function: Test function for the page.
    """
    def test(self):
        """Test function for accessing a page successfully.

        Args:
            self (class): self
        """
        self.client = Client()
        if auth:
            user = User.objects.create(username='user', password='user')
            models.Client.objects.create(user=user)
            self.client.force_login(user)

        reversed_url = reverse(page_name)
        if page_name == 'join':
            club = models.Club.objects.create(name='name', phone_number='+79098087060')
            url, reversed_url = f'{page_url}?id={club.id}', f'{reversed_url}?id={club.id}'
        else:
            url = page_url

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, template)

        response = self.client.get(reversed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    return test


def create_redirect_page_test(page_name):
    """Create a test function for redirecting to login page.

    Args:
        page_name (str): Name of the page.

    Returns:
        function: Test function for page redirection.
    """
    def test(self):
        """Test function for page redirection.

        Args:
            self (class): self
        """
        self.client = Client()
        self.client.logout()

        self.assertEqual(self.client.get(reverse(page_name)).status_code, status.HTTP_302_FOUND)

    return test


auth_pages = (
    ('/clubs/', 'clubs', 'catalog/clubs.html'),
    ('/boardgames/', 'boardgames', 'catalog/boardgames.html'),
    ('/addresses/', 'addresses', 'catalog/addresses.html'),
    ('/club/', 'club', 'entities/club.html'),
    ('/boardgame/', 'boardgame', 'entities/boardgame.html'),
    ('/address/', 'address', 'entities/address.html'),
    ('/profile/', 'profile', 'pages/profile.html'),
    ('/join/', 'join', 'pages/join.html'),
)

casual_pages = (
    ('/register/', 'register', 'registration/register.html'),
    ('', 'homepage', 'index.html'),
    ('/accounts/login/', 'login', 'registration/login.html'),
)

casual_methods = {f'test_{page[1]}': create_successful_page_test(*page) for page in casual_pages}
TestCasualPages = type('TestCasualPages', (TestCase,), casual_methods)

auth_pages_methods = {f'test_{page[1]}': create_successful_page_test(*page) for page in auth_pages}
TestAuthPages = type('TestAuthPages', (TestCase,), auth_pages_methods)

no_auth_pages_methods = {f'test_{page}': create_redirect_page_test(page) for _, page, _ in auth_pages}
TestNoAuthPages = type('TestNoAuthPages', (TestCase,), no_auth_pages_methods)
