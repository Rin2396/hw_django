"""Tests for api."""

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from main_game.models import BoardGame, Club, GameSet


def create_api_test(model, url, creation_attrs):
    """Create API test cases for a specific model.

    Args:
        model (class): django model class for tested.
        url (str): base URL endpoint for the API.
        creation_attrs (dict): attributes for creating via API.

    Returns:
        class: TestCase class containing API test methods.
    """
    class ApiTest(TestCase):
        """Test cases for API endpoints related to a specific model.

        Args:
            TesyCase (class): django class for tests.
        """

        def setUp(self) -> None:
            """Set up the test environment."""
            self.client = APIClient()

            self.user = User.objects.create(username='abc', password='abc')
            self.superuser = User.objects.create(
                username='admin', password='admin', is_superuser=True,
            )

            self.user_token = Token.objects.create(user=self.user)
            self.superuser_token = Token.objects.create(user=self.superuser)

        def manage(
            self, user: User,
            token: Token,
            post_expected: int,
            put_expected: int,
            delete_expected: int,
        ):
            """Perform CRUD operations via API with given user and token.

            Args:
                user (User): performing the operation.
                token (Token): for user authentication.
                post_expected (int): expected status code for POST.
                put_expected (int): expected status code for PUT.
                delete_expected (int): expected status code for DELETE.
            """
            self.client.force_authenticate(user=user, token=token)

            self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.head(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.options(url).status_code, status.HTTP_200_OK)

            post_response = self.client.post(url, creation_attrs)
            self.assertEqual(post_response.status_code, post_expected)

            created_id = model.objects.create(**creation_attrs).id
            instance_url = f'{url}{created_id}/'
            put_response = self.client.put(instance_url, creation_attrs)
            self.assertEqual(put_response.status_code, put_expected)

            delete_response = self.client.delete(instance_url)
            self.assertEqual(delete_response.status_code, delete_expected)

        def test_superuser(self):
            """Test API operations with superuser permissions."""
            self.manage(
                self.superuser, self.superuser_token,
                post_expected=status.HTTP_201_CREATED,
                put_expected=status.HTTP_200_OK,
                delete_expected=status.HTTP_204_NO_CONTENT,
            )

        def test_user(self):
            """Test API operations with regular user permissions."""
            self.manage(
                self.user, self.user_token,
                post_expected=status.HTTP_403_FORBIDDEN,
                put_expected=status.HTTP_403_FORBIDDEN,
                delete_expected=status.HTTP_403_FORBIDDEN,
            )

    return ApiTest


url = '/api/'
ClubApiTest = create_api_test(Club, f'{url}clubs/', {'name': 'abc', 'phone_number': '+79999999999'})
BoardGameApiTest = create_api_test(BoardGame, f'{url}boardgames/', {'name': 'def', 'level': 1})
GameSetApiTest = create_api_test(GameSet, f'{url}game_sets/', {'name': 'ghi'})
