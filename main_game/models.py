"""Models file."""
import re
from datetime import datetime, timezone
from uuid import uuid4

from django.conf.global_settings import AUTH_USER_MODEL
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

NAME_MAX_LEN = 100
ADDRESS_MAX_LEN = 100
PHONE_MAX_LEN = 12
DESCRIPTION_MAX_LEN = 1000


class UUIDMixin(models.Model):
    """Mixin class providing UUID primary key field."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        """Meta class."""

        abstract = True


def get_datetime():
    """Return the current UTC date and time.

    Returns:
        datetime: current date and time
    """
    return datetime.now(timezone.utc)


def check_created(dt: datetime):
    """Validate created datetime.

    Args:
        dt (datetime): The datetime to validate.

    Raises:
        ValidationError: If the datetime is in the future.
    """
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time cannot be in the future.'),
            params={'created': dt},
        )


def check_modified(dt: datetime):
    """Validate modified datetime.

    Args:
        dt (datetime): The datetime to validate.

    Raises:
        ValidationError: If the datetime is in the future.
    """
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time cannot be in the future.'),
            params={'modified': dt},
        )


def check_level(number) -> None:
    """Validate game level.

    Args:
        number (int): The level of the game.

    Raises:
        ValidationError: If the level is not within the valid range (0-100).
    """
    if number < 0 or number > 100:
        raise ValidationError('Value should be between zero and one hundred.')


def phone_number_validator(number: str) -> None:
    """Validate phone number format.

    Args:
        number (str): The phone number to validate.

    Raises:
        ValidationError: If the phone number format is invalid.
    """
    rule = re.compile(r'^\+7[0-9]{3}[0-9]{7}$')
    if not rule.search(number):
        raise ValidationError(
            _('Phone number must be in the format +79999999999.'),
            params={'phone_number': number},
        )


class CreatedMixin(models.Model):
    """Mixin class providing created datetime field."""

    created = models.DateTimeField(
        _('created'),
        null=True, blank=True,
        default=get_datetime,
        validators=[check_created],
    )

    class Meta:
        """Meta class."""

        abstract = True


class ModifiedMixin(models.Model):
    """Mixin class providing modified datetime field."""

    modified = models.DateTimeField(
        _('modified'),
        null=True, blank=True,
        default=get_datetime,
        validators=[check_modified],
    )

    class Meta:
        """Meta class."""

        abstract = True


class Club(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model class for a club.

    Args:
        UUIDMixin (class): Mixin class providing UUID primary key field.
        CreatedMixin (class): Mixin class providing created datetime field.
        ModifiedMixin (class): Mixin class providing modified datetime field.

    Returns:
        str: String representation of the club.
    """

    name = models.TextField(_('name'), null=False, blank=False, max_length=ADDRESS_MAX_LEN)
    phone_number = models.TextField(_('phone_number'), null=False, blank=False, validators=[phone_number_validator])

    games = models.ManyToManyField('BoardGame', through='ClubToGame')
    addresses = models.ManyToManyField('Address', through='ClubAddress')

    def __str__(self) -> str:
        """Return a string representation of the club.

        Returns:
            str: name of club
        """
        return self.name

    class Meta:
        """Meta class."""

        db_table = '"game_site"."clubs"'
        ordering = ['name']
        verbose_name = _('club')


class BoardGame(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model class for a board game.

    Args:
        UUIDMixin (class): Mixin class providing UUID primary key field.
        CreatedMixin (class): Mixin class providing created datetime field.
        ModifiedMixin (class): Mixin class providing modified datetime field.

    Returns:
        str: String representation of the board game.
    """

    name = models.TextField(_('name'), null=False, blank=False, max_length=NAME_MAX_LEN)
    level = models.PositiveIntegerField(_('level'), null=False, blank=False, validators=[check_level])

    genres = models.ManyToManyField('Genre', through='GameGenre')
    clubs = models.ManyToManyField('Club', through='ClubToGame')
    sets = models.ManyToManyField('GameSet', through='SetToGame')

    def __str__(self) -> str:
        """Return a string representation of the board game.

        Returns:
            str: name of game
        """
        return self.name

    class Meta:
        """Meta class."""

        db_table = '"game_site"."boardgames"'
        ordering = ['name']
        verbose_name = _('boardgame')


class Genre(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model class for a genre.

    Args:
        UUIDMixin (class): Mixin class providing UUID primary key field.
        CreatedMixin (class): Mixin class providing created datetime field.
        ModifiedMixin (class): Mixin class providing modified datetime field.

    Returns:
        str: String representation of the genre.
    """

    name = models.TextField(_('name'), null=False, blank=False, max_length=NAME_MAX_LEN, default='no genre')
    description = models.TextField(_('description'), null=True, blank=True, max_length=DESCRIPTION_MAX_LEN)

    games = models.ManyToManyField('BoardGame', through='GameGenre')

    def __str__(self) -> str:
        """Return a string representation of the genre.

        Returns:
            str: genre info
        """
        return f'{self.name}: {self.description}'

    class Meta:
        """Meta class."""

        db_table = '"game_site"."genres"'
        ordering = ['name']
        verbose_name = _('genre')


class Address(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model class for an address.

    Args:
        UUIDMixin (class): Mixin class providing UUID primary key field.
        CreatedMixin (class): Mixin class providing created datetime field.
        ModifiedMixin (class): Mixin class providing modified datetime field.

    Returns:
        str: String representation of the address.
    """

    region = models.TextField(_('region'), null=False, blank=False, max_length=NAME_MAX_LEN)
    city = models.TextField(_('city'), null=False, blank=True, default='Sirius', max_length=NAME_MAX_LEN)
    street = models.TextField(_('street'), null=True, blank=True, max_length=NAME_MAX_LEN)
    home = models.TextField(_('home'), null=True, blank=True, max_length=NAME_MAX_LEN)

    clubs = models.ManyToManyField('Club', through='ClubAddress')

    def __str__(self) -> str:
        """Return a string representation of the address.

        Returns:
            str: full address
        """
        return f'{self.region}, {self.city}, {self.street}, {self.home}'

    class Meta:
        """Meta class."""

        db_table = '"game_site"."addresses"'
        ordering = ['region', 'city', 'street']
        verbose_name = _('address')
        verbose_name_plural = _('addresses')


class GameSet(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model class for a game set.

    Args:
        UUIDMixin (class): Mixin class providing UUID primary key field.
        CreatedMixin (class): Mixin class providing created datetime field.
        ModifiedMixin (class): Mixin class providing modified datetime field.

    Returns:
        str: String representation of the game set.
    """

    name = models.TextField(_('name'), null=False, blank=False, max_length=NAME_MAX_LEN)
    description = models.TextField(_('description'), null=False, blank=True, default='', max_length=DESCRIPTION_MAX_LEN)

    games = models.ManyToManyField('BoardGame', through='SetToGame')

    def __str__(self) -> str:
        """Return a string representation of the game set.

        Returns:
            str: game set
        """
        return f'{self.name}: {self.description}'

    class Meta:
        """Meta class."""

        db_table = '"game_site"."game_sets"'
        ordering = ['name']
        verbose_name = _('game_set')


class ClubToGame(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model class representing the relationship between clubs and board games.

    Args:
        club (Club): Club related to the relationship
        game (BoardGame): Board game related to the relationship

    Returns:
        str: String representation of the relationship between a club and a board game
    """

    club = models.ForeignKey(Club, verbose_name=_('club'), on_delete=models.CASCADE)
    game = models.ForeignKey(BoardGame, verbose_name=_('boardgames'), on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return a string representation of the relationship.

        Returns:
            str: club and game
        """
        return f'club {self.club} - game {self.game}'

    class Meta:
        """Meta class."""

        db_table = '"game_site"."club_to_game"'
        unique_together = (
            ('club', 'game'),
        )
        verbose_name = _('Relationship club game')


class SetToGame(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model class representing the relationship between game sets and board games.

    Args:
        set (GameSet): Game set related to the relationship
        game (BoardGame): Board game related to the relationship

    Returns:
        str: String representation of the relationship between a game set and a board game
    """

    set = models.ForeignKey(GameSet, verbose_name=_('game_set'), on_delete=models.CASCADE)
    game = models.ForeignKey(BoardGame, verbose_name=_('boardgames'), on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return a string representation of the relationship.

        Returns:
            str: set and game
        """
        return f'set {self.set} - game {self.game}'

    class Meta:
        """Meta class."""

        db_table = '"game_site"."set_to_game"'
        unique_together = (
            ('set', 'game'),
        )
        verbose_name = _('Relationship set game')


class GameGenre(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model class representing the relationship between board games and genres.

    Args:
        game (BoardGame): Board game related to the relationship
        genre (Genre): Genre related to the relationship

    Returns:
        str: String representation of the relationship between a board game and a genre
    """

    game = models.ForeignKey(BoardGame, verbose_name=_('boardgames'), on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, verbose_name=_('genre'), on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return a string representation of the relationship.

        Returns:
            str: game and genre
        """
        return f'game {self.game} - genre {self.genre}'

    class Meta:
        """Meta class."""

        db_table = '"game_site"."game_genre"'
        unique_together = (
            ('game', 'genre'),
        )
        verbose_name = _('Relationship game genre')


class ClubAddress(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model class representing the relationship between clubs and addresses.

    Args:
        club (Club): Club related to the relationship
        address (Address): Address related to the relationship

    Returns:
        str: String representation of the relationship between a club and an address
    """

    club = models.ForeignKey(Club, verbose_name=_('club'), on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name=_('address'), on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return a string representation of the relationship.

        Returns:
            str: club and address
        """
        return f'club {self.club} - address {self.address}'

    class Meta:
        """Meta class."""

        db_table = '"game_site"."club_address"'
        unique_together = (
            ('club', 'address'),
        )
        verbose_name = _('Relationship club address')


def create_manager(validators: tuple[tuple[str, callable]]):
    """Create a custom manager for models.

    Args:
        validators (tuple[tuple[str, callable]]): Tuple of attribute names and corresponding validators

    Returns:
        Manager: Custom manager class
    """

    class Manager(models.Manager):
        """Custom manager class."""

        @staticmethod
        def check_and_validate(kwargs, value, validator):
            """Check and validate attributes.

            Args:
                kwargs (any): kwargs
                value (any): value
                validator (any): validator
            """
            if value in kwargs.keys():
                validator(kwargs.get(value))

        def create(self, **kwargs):
            """Override create method to include validation.

            Args:
                kwargs (any): kwargs

            Returns:
                function: create function
            """
            for value, validator in validators:
                self.check_and_validate(kwargs, value, validator)
            return super().create(**kwargs)

    return Manager


def create_save(validators: tuple[tuple[str, callable]]):
    """Create a custom save method for models.

    Args:
        validators (tuple[tuple[str, callable]]): Tuple of attribute names and corresponding validators

    Returns:
        function: Custom save method
    """

    def save(self, *args, **kwargs) -> None:
        """Override save method to include validation.

        Args:
            kwargs (any): kwargs
            args (any): arguments
            self (any): class self

        Returns:
            function: save function
        """
        for value, validator in validators:
            validator(getattr(self, value))
        return super(self.__class__, self).save(*args, **kwargs)

    return save


class Client(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model class representing a client/user in the system.

    Args:
        user (User): User associated with the client
        clubs (ManyToManyField): Clubs associated with the client
        objects (Manager): Custom manager with validation methods
        save (function): Custom save method with validation

    Returns:
        str: String representation of the client
    """

    user = models.OneToOneField(AUTH_USER_MODEL, unique=True, verbose_name=_('user'), on_delete=models.CASCADE)
    clubs = models.ManyToManyField(Club, through='ClubClient', verbose_name=_('clubs'))
    objects = create_manager((('created', check_created), ('modified', check_modified)))
    save = create_save((('created', check_created), ('modified', check_modified)))

    class Meta:
        """Meta class."""

        db_table = '"game_site"."client"'
        verbose_name = _('client')
        verbose_name_plural = _('clients')

    @property
    def username(self) -> str:
        """Property to get the username of the associated user.

        Returns:
            str: username
        """
        return self.user.username

    @property
    def first_name(self) -> str:
        """Property to get the first name of the associated user.

        Returns:
            str: first name
        """
        return self.user.first_name

    @property
    def last_name(self) -> str:
        """Property to get the last name of the associated user.

        Returns:
            str: last name
        """
        return self.user.last_name

    def __str__(self) -> str:
        """Represent of the client.

        Returns:
            str: string representation
        """
        return f'{self.username} ({self.first_name} {self.last_name})'


class ClubClient(UUIDMixin, CreatedMixin):
    """Model class representing the relationship between clubs and clients.

    Args:
        club (Club): Club related to the relationship
        client (Client): Client related to the relationship

    Returns:
        str: String representation of the relationship between a club and a client
    """

    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name=_('club'))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('client'))

    class Meta:
        """Meta class."""

        db_table = '"game_site"."club_client"'
        verbose_name = _('relationship club client')
        verbose_name_plural = _('relationships club client')
