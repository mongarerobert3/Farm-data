# dairy_management/urls.py
from django.contrib import admin
from django.urls import path
from .views import add_user, delete_user

urlpatterns = [
    #path('add-doctor/', add_doctor, name='add_doctor'),
    path('add-user/', add_user, name='add_user'),
    #path('admins/', all_admins, name='all_admins'),
    #path('update-user/<str:id>/', update_user, name='update_user'),

    path('<uuid:id>/delete/', delete_user, name='delete_user'),
    #path('logout/', user_logout_view, name='logout'),
    #path('register/', user_register_user, name='register'),
]
