"""Serializers file."""
from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Address, BoardGame, Club, GameSet, Genre


class ClubSerializer(HyperlinkedModelSerializer):
    """Serializer for Club."""

    class Meta:
        """Meta class for ClubSerializer."""

        model = Club
        fields = [
            'id',
            'name',
            'phone_number',
            'games',
            'addresses',
        ]


class BoardGameSerializer(HyperlinkedModelSerializer):
    """Serializer for BoardGame."""

    class Meta:
        """Meta class for BoardGameSerializer."""

        model = BoardGame
        fields = [
            'id',
            'name',
            'genres',
            'level',
            'clubs',
        ]


class GameSetSerializer(HyperlinkedModelSerializer):
    """Serializer for GameSet."""

    class Meta:
        """Meta class for GameSetSerializer."""

        model = GameSet
        fields = [
            'id',
            'name',
            'description',
            'games',
        ]


class GenreSerializer(HyperlinkedModelSerializer):
    """Serializer for Genre."""

    class Meta:
        """Meta class for GenreSerializer."""

        model = Genre
        fields = '__all__'


class AddressSerializer(HyperlinkedModelSerializer):
    """Serializer for Address."""

    class Meta:
        """Meta class for AddressSerializer."""

        model = Address
        fields = '__all__'
