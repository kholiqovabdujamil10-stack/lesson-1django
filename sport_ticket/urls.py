from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('registration/', registration, name='registration'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),

    path('games/', games, name='games'),
    path('create_game/', create_game, name='create_game'),
    path('edit_game/<int:id>/', edit_game, name='edit_game'),
    path('delete_game/<int:id>/', delete_game, name='delete_game'),

    path('buy_ticket/<int:id>/', buy_ticket, name='buy_ticket'),
    path('my_tickets/', my_tickets, name='my_tickets'),
    path('cancel_ticket/<int:id>/', cancel_ticket, name='cancel_ticket'),
]