from django.contrib import admin
from django.urls import path

from . import views

app_name = 'list'

urlpatterns = [
    path('<int:pk>/get/', views.ListGetLinks.as_view(), name='get_links'),
    path('<uuid:pk>/edit/', views.ListEditLinks.as_view(), name='edit_link'),
    path('<uuid:pk>/delete/', views.ListDeleteLink.as_view(), name='delete_link'),

    path('save/', views.ListSaveLinks.as_view(), name='save_links'),
    path('create/', views.ListCreateLink.as_view(), name='create_link'),
    path('<int:pk>/show/', views.ListShowLinks.as_view(), name='show_links_tab'),

    
]
