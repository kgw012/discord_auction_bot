from django.urls import path

from . import views
urlpatterns = [
    path('player/', views.player_list_create),
]
