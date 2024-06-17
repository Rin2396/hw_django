"""Admin file."""

from django.contrib import admin

from .models import (Address, BoardGame, Client, Club, ClubAddress, ClubClient,
                     ClubToGame, GameGenre, GameSet, Genre, SetToGame)


class ClubToGameInline(admin.TabularInline):
    """Inline class for ClubToGame.

    Args:
        admin: django admin
    """

    model = ClubToGame
    extra = 1


class SetToGameInline(admin.TabularInline):
    """Inline class for SetToGame.

    Args:
        admin: django admin
    """

    model = SetToGame
    extra = 1


class GameGenreInline(admin.TabularInline):
    """Inline class for GameGenre.

    Args:
        admin: django admin
    """

    model = GameGenre
    extra = 1


class ClubAddressInline(admin.TabularInline):
    """Inline class for ClubAddress.

    Args:
        admin: django admin
    """

    model = ClubAddress
    extra = 1


class ClubClientInline(admin.TabularInline):
    """Inline class for ClubClient.

    Args:
        admin: django admin
    """

    model = ClubClient
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Admin class for Client.

    Args:
        admin: django admin
    """

    model = Client
    inlines = (ClubClientInline,)


@admin.register(BoardGame)
class BoardGameAdmin(admin.ModelAdmin):
    """Admin class for BoardGame.

    Args:
        admin: django admin
    """

    model = BoardGame
    search_fields = ['name', 'genre', 'level']
    inlines = (ClubToGameInline, SetToGameInline, GameGenreInline)


@admin.register(GameSet)
class GameSetAdmin(admin.ModelAdmin):
    """Admin class for GameSet.

    Args:
        admin: django admin
    """

    model = GameSet
    search_fields = ['name']
    inlines = (SetToGameInline,)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Admin class for Club.

    Args:
        admin: django admin
    """

    model = Club
    search_fields = ['name', 'address', 'phone_number']
    inlines = (ClubToGameInline, ClubAddressInline)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin class for Address.

    Args:
        admin: django admin
    """

    model = Address
    inlines = (ClubAddressInline,)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin class for Genre.

    Args:
        admin: django admin
    """

    model = Genre
    inlines = (GameGenreInline,)
