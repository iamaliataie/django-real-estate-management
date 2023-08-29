from django.urls import path
from . import views

app_name = 'inquiry'

urlpatterns = [
    path('inquiries/',
         views.InquiryListView.as_view(), 
         name='inquiry_list'
    ),
    path(
        'inquiries/<int:pk>',
        views.InquiryDetailView.as_view(),
        name='inquiry_detail',
    ),
]