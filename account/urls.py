from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from . import views

app_name = 'accounts'

urlpatterns = [
    path(
        'property/create/',
        views.PropertyCreate.as_view(),
        name='property_create'
    ),
    path(
        'property/update/<int:pk>/',
        views.PropertyUpdate.as_view(),
        name='property_update'
    ),
    path(
        'property/remove_property_image/<int:pk>/',
        views.remove_property_image,
        name='remove_property_image'
    ),
    path(
        'properties/agent/',
        views.AgentPropertyListView.as_view(),
        name='agent_property_list'
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
    path(
        'reset/',
        PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')),
        name='password_reset'
    ),
    path(
        'reset/done/',
        PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete')),
        name='password_reset_confirm'
    ),
    path(
        'reset/complete/',
        PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]