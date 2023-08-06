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
        'properties/',
        views.PropertyListView.as_view(),
        name='property_list'
    ),
    path(
        'properties/<int:pk>',
        views.PropertyDetailView.as_view(),
        name='property_detail'
    ),
    path(
        'add_to_favorites/',
        views.add_to_favorites,
        name='add_to_favorites'
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