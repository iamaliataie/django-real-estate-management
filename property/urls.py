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
        'about/',
        views.About.as_view(),
        name='about'
    ),
    path(
        'search/',
        views.search_ajax,
        name='search'
    ),
    path(
        'properties/',
        views.PropertyListView.as_view(),
        name='property_list'
    ),
    path(
        'properties/<int:pk>/',
        views.PropertyDetailView.as_view(),
        name='property_detail'
    ),
    path(
        'properties/<str:slug>/',
        views.TypePropertyListView.as_view(),
        name='type_property_list'
    ),
    path(
        'add_to_favorites/',
        views.add_to_favorites,
        name='add_to_favorites'
    ),
]