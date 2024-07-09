# dairy/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ProductionRecord URLs
		path('production-records/create/', views.create_production_record, name='create_production_record'),
    path('production-records/', views.list_production_records, name='list_production_records'),
    path('production-records/<str:cow_id>/', views.detail_production_record, name='detail_production_record'),
    path('production-records/update/<str:id>/', views.update_production_record, name='update_production_record'),
    path('production-records/delete/<str:id>/', views.delete_production_record, name='delete_production_record'),
		
    path('all-milk/', views.total_collected_milk, name='total_collected_milk'),
    path('milk-data/', views.total_milk_data, name='total_milk_data'),

    # FeedingRecord URLs
    path('feeding-records/', views.list_feeding_records, name='list_feeding_records'),
    path('feeding-records/<int:id>/', views.detail_feeding_record, name='detail_feeding_record'),
    path('feeding-records/add/', views.create_feeding_record, name='add_feeding_record'),
    path('feeding-records/update/<int:id>/', views.update_feeding_record, name='update_feeding_record'),
    path('feeding-records/delete/<int:id>/', views.delete_feeding_record, name='delete_feeding_record'),
]
