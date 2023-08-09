from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path(
        'property/create/',
        views.PropertyCreate.as_view(),
        name='property_create'
    ),
    path(
        'property/update/<int:pk>',
        views.PropertyUpdate.as_view(),
        name='property_update'
    ),
    path(
        'bookmarks/',
        views.BookmarkView.as_view(),
        name='bookmarks'
    ),
    path(
        'bookmarks/remove_from_bookmarks/<int:pk>/',
        views.remove_from_bookmarks,
        name='remove_from_bookmarks'
    ),
    path(
        'login/',
        views.Login.as_view(),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        'register/',
        views.Register.as_view(),
        name='register'
    ),
    path(
        'activate/<uidb64>/<token>/',
        views.activate,
        name='activate'
    ),
]