from django.urls import path
from . import views

urlpatterns = [
	path('', views.all_cows, name='all_cows'),
	path('<uuid:cow_id>/', views.search_cow, name='search_cow'),
	path('add/', views.create_cow, name='create_cow'),
	path('<uuid:cow_id>/edit/', views.search_cow, name='search_cow'),
	path('<uuid:cow_id>/delete/', views.delete_cow, name='delete_cow'),
	path('vaccinate/<str:cow_id>/', views.vaccinate_cow, name='vaccinate_cow'),
]