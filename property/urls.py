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
        'properties',
        views.PropertyListView.as_view(),
        name='property_list'
    ),
    path(
        'properties/<int:pk>',
        views.PropertyDetailView.as_view(),
        name='property_detail'
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