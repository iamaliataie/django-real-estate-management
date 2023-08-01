from django.urls import path
from . import views

app_name = 'property'

urlpatterns = [
    path(
        '',
        views.Home.as_view(),
        name='home'
    ),
    path(
        'create/',
        views.PropertyCreate.as_view(),
        name='create'
    ),
    path(
        'update/<int:pk>/',
        views.PropertyUpdate.as_view(),
        name='update'
    ),
]