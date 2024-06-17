"""Views file."""
from typing import Any

from django.contrib import messages
from django.contrib.auth import decorators, mixins
from django.core import exceptions
from django.core import paginator as pg
from django.shortcuts import redirect, render
from django.views.generic import ListView
from rest_framework import authentication, permissions, viewsets

from .forms import Join, Registration
from .models import (Address, BoardGame, Client, Club, ClubClient, GameSet,
                     Genre)
from .serializers import (AddressSerializer, BoardGameSerializer,
                          ClubSerializer, GameSetSerializer, GenreSerializer)


def home(request):
    """Render the homepage view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered response of the homepage view.
    """
    return render(
        request,
        'index.html',
        {
            'clubs': Club.objects.count(),
            'boardgames': BoardGame.objects.count(),
            'genres': Genre.objects.count(),
            'gamesets': GameSet.objects.count(),
            'addresses': Address.objects.count(),
        },
    )


def create_list_view(model_class, plural_name, template):
    """Create a ListView class for a given model.

    Args:
        model_class (class): The Django model class to create ListView for.
        plural_name (str): The plural name of the model (context object name).
        template (str): The path to the template to render the ListView.

    Returns:
        class: Custom ListView class for the given model.
    """

    class CustomListView(mixins.LoginRequiredMixin, ListView):
        """Custom ListView class."""

        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            """Override get_context_data to add pagination.

            Args:
                kwargs (any): kwargs

            Returns:
                dict[str, Any]: context data
            """
            context = super().get_context_data(**kwargs)
            clubs = model_class.objects.all()
            paginator = pg.Paginator(clubs, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context

    return CustomListView


СlubListView = create_list_view(Club, 'clubs', 'catalog/clubs.html')
BoardGameListView = create_list_view(BoardGame, 'boardgames', 'catalog/boardgames.html')
GameSetListView = create_list_view(GameSet, 'gamesets', 'catalog/gamesets.html')
AddressListView = create_list_view(Address, 'addresses', 'catalog/addresses.html')
GenreListView = create_list_view(Genre, 'genres', 'catalog/genres.html')


def create_view(model_class, context_name, template):
    """Create a view function for rendering a single instance of a model.

    Args:
        model_class (class): The Django model class to create the view for.
        context_name (str): The context name for the model instance.
        template (str): The path to the template to render the model instance.

    Returns:
        function: View function for rendering a single model instance.
    """

    @decorators.login_required
    def view(request):
        """View function to render a single instance of a model.

        Args:
            request (any): request

        Returns:
            HttpResponse: Rendered response of the homepage view.
        """
        id_ = request.GET.get('id', None)
        target = model_class.objects.get(id=id_) if id_ else None
        return render(request, template, {context_name: target})

    return view


сlub_view = create_view(Club, 'club', 'entities/club.html')
boardgame_view = create_view(BoardGame, 'boardgame', 'entities/boardgame.html')
gameset_view = create_view(GameSet, 'gameset', 'entities/gameset.html')
address_view = create_view(Address, 'address', 'entities/address.html')
genre_view = create_view(Genre, 'genre', 'entities/genre.html')


def register(request):
    """Handle user registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered response of the registration view.
    """
    errors = ''
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
        else:
            errors = form.errors
    else:
        form = Registration()

    return render(
        request,
        'registration/register.html',
        {
            'form': form,
            'errors': errors,
        },
    )


class MyPermission(permissions.BasePermission):
    """Custom permission class to define permissions based on request method."""

    _safe_methods = 'GET', 'HEAD', 'OPTIONS', 'PATCH'
    _unsafe_methods = 'POST', 'PUT', 'DELETE'

    def has_permission(self, request, _):
        """Check if the request has permission.

        Args:
            request (HttpRequest): The HTTP request object.
            _: Unused argument.

        Returns:
            bool: True if request has permission, False otherwise.
        """
        if request.method in self._safe_methods and (request.user and request.user.is_authenticated):
            return True
        if request.method in self._unsafe_methods and (request.user and request.user.is_superuser):
            return True
        return False


def create_viewset(model_class, serializer):
    """Create a ViewSet class for a given model and serializer.

    Args:
        model_class (class): The Django model class to create ViewSet for.
        serializer (Serializer): The DRF serializer class for the model.

    Returns:
        class: Custom ViewSet class for the given model.
    """

    class CustomViewSet(viewsets.ModelViewSet):
        """Custom ViewSet class."""

        serializer_class = serializer
        queryset = model_class.objects.all()
        permission_classes = [MyPermission]
        authentication_classes = [authentication.TokenAuthentication]

    return CustomViewSet


ClubViewSet = create_viewset(Club, ClubSerializer)
BoardGameViewSet = create_viewset(BoardGame, BoardGameSerializer)
GameSetViewSet = create_viewset(GameSet, GameSetSerializer)
GenreViewSet = create_viewset(Genre, GenreSerializer)
AddressViewSet = create_viewset(Address, AddressSerializer)


@decorators.login_required
def profile(request):
    """Render the user profile view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered response of the user profile view.
    """
    client = Client.objects.get(user=request.user)
    form_errors = ''

    if request.method == 'POST':
        form = Join(request.POST)
        if form.is_valid():
            club = form.cleaned_data.get('club')
            if club:
                if not ClubClient.objects.filter(club=club, client=client).exists():
                    ClubClient.objects.create(club=club, client=client)
                else:
                    form_errors = 'You already joined this club!'
            else:
                form_errors = 'The club is not listed!'
        else:
            form_errors = 'Form validation error!'
    else:
        form = Join()

    client_attrs = ['username', 'first_name', 'last_name']
    client_data = {attr: getattr(client, attr) for attr in client_attrs}
    return render(
        request,
        'pages/profile.html',
        {
            'client_data': client_data,
            'form': form,
            'form_errors': form_errors,
            'client_clubs': client.clubs.all(),
        },
    )


@decorators.login_required
def join(request):
    """Handle joining a club by a user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered response of the join club view.
    """
    client = Client.objects.get(user=request.user)
    id_ = request.GET.get('id', None)
    if not id_:
        return redirect('clubs')
    try:
        club = Club.objects.get(id=id_)
    except (exceptions.ValidationError, exceptions.ObjectDoesNotExist):
        return redirect('clubs')
    if not club:
        return redirect('clubs')
    if club in client.clubs.all():
        return redirect('profile')

    if request.method == 'POST':
        client.clubs.add(club)
        client.save()
        return redirect('profile')

    return render(
        request,
        'pages/join.html',
        {
            'club': club,
        },
    )


@decorators.login_required
def remove_from_joined(request, club_id):
    """Handle removing a club from joined clubs by a user.

    Args:
        request (HttpRequest): The HTTP request object.
        club_id (int): The ID of the club to be removed from joined clubs.

    Returns:
        HttpResponse: Redirects to user profile page after removing the club.
    """
    client = Client.objects.get(user=request.user)
    try:
        club_client = ClubClient.objects.get(client=client, club_id=club_id)
        club_client.delete()
        messages.success(request, 'You have successfully left the club.')
    except ClubClient.DoesNotExist:
        messages.error(request, 'You are not a member of this club.')
    except Exception as exc:
        messages.error(request, f'An error occurred: {exc}')

    return redirect('profile')
