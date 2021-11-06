from django.urls import path

from . import views
urlpatterns = [
    # player C,R,D
    path('players', views.player_list_create),
    path('players/<int:player_pk>', views.player_get_delete),
    
    # item C,R,D
    path('items', views.item_list),
    path('players/<int:player_pk>/items', views.item_create),
    path('players/<int:player_pk>/items/<int:item_pk>', views.item_get_delete),
    
    # bid C,D
    # path('players/<int:player_pk>/bid/<int:item_pk>', views.bid_create),
]
