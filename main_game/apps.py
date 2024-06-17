"""Apps file."""
from django.apps import AppConfig


class MainGameConfig(AppConfig):
    """AppConfig class for main_game."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_game'
