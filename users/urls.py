from django.contrib import admin
from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UsersRegisterUser.as_view(), name='user_register'),

    path('activate/<uidb64>/<token>/', views.UsersActivateUser.as_view(), name='user_activate'),
    path('forgot/', views.UsersForgotPassword.as_view(), name='forgot_password'),
    path('reset/<uidb64>/<token>/', views.UsersResetPassword.as_view(), name='reset_password'),

    path('search', views.UsersSearch.as_view(), name='search'),

    path('<int:pk>/', views.UsersViewProfile.as_view(), name='view_profile'),
    path('<int:pk>/edit/', views.edit_profile, name='edit_profile'),
    path('<int:pk>/get/', views.get_profile, name='get_profile'),
    path('<int:pk>/change_password/', views.change_password, name='change_password'),

    path('<int:pk>/short_bio/', views.UsersViewShortIntro.as_view(), name='view_short_intro'),
    path('<int:pk>/short_bio/edit', views.UsersEditShortIntro.as_view(), name='edit_short_intro'),
    
    path("qrcode/download", views.DownloadQRCode.as_view(), name='download_qrcode'),
    
]
""" path('users/', views.UsersViewAll.as_view(), name='users'),
    path('users/<int:pk>/', views.UsersViewUser.as_view(), name='user_view'),
    path('users/edit/<int:pk>/', views.UsersEditUser.as_view(), name='user_edit'),
    path('users/delete/<int:pk>/', views.UsersDeleteUser.as_view(), name='user_delete'),
    path('users/create/', views.UsersCreateUser.as_view(), name='user_create'),
    path('users/invite/', views.UsersInviteUser.as_view(), name='user_invite'),
    path('users/reset-password/<int:pk>/', views.UsersResetPassword.as_view(), name='user_reset_password'),
    path('users/create-password/<uuid:uuid>/', views.UsersCreatePassword.as_view(), name='user_create_password'),
    path('profile/<int:pk>/', views.ProfileViewProfile.as_view(), name='view_profile'),
    path('users/register/', views.UsersRegisterUser.as_view(), name='user_register'), """