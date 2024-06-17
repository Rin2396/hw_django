"""Urls file."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'clubs', views.ClubViewSet)
router.register(r'boardgames', views.BoardGameViewSet)
router.register(r'game_sets', views.GameSetViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'addresses', views.AddressViewSet)


urlpatterns = [
    path('', views.home, name='homepage'),
    path('clubs/', views.СlubListView.as_view(), name='clubs'),
    path('club/', views.сlub_view, name='club'),
    path('boardgames/', views.BoardGameListView.as_view(), name='boardgames'),
    path('boardgame/', views.boardgame_view, name='boardgame'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('genre/', views.genre_view, name='genre'),
    path('addresses/', views.AddressListView.as_view(), name='addresses'),
    path('address/', views.address_view, name='address'),
    path('gamesets/', views.GameSetListView.as_view(), name='gamesets'),
    path('gameset/', views.gameset_view, name='gameset'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls), name='api'),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),
    path('profile/', views.profile, name='profile'),
    path('join/', views.join, name='join'),
    path('remove_from_joined/<uuid:club_id>/', views.remove_from_joined, name='remove_from_joined'),
]
