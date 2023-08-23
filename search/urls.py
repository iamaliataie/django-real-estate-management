from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path(
        'clear_search/',
        views.clear_user_search,
        name='clear_user_search'
    ),
]