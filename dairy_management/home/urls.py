from django.urls import path, include
from .views import cows, sale_cow_report, sale_cow, sale_milk_report, create_sales, sale_milk, dashboard, staffinfo, dashboard_view, home, custom_login, vaccine_page

urlpatterns = [
	path('', home, name='home' ),
	path('login/', custom_login, name='login' ),
	path('accounts/', include('allauth.urls')),
	path('prod/dashboard/', dashboard, name='dashboard'),
	path('staff/', staffinfo, name='staff'),
	path('cows/', cows, name='cows'),
	path('dashboard/', dashboard_view, name='dashboard_view'),
	path('vaccines/', vaccine_page, name='vaccines'),
	path('sales/create/', create_sales, name='create-sales'),
	path('sales/', sale_milk, name='sale_milk'),
	path('sale-milk-report/', sale_milk_report, name='sale_milk_report'),
	path('sale-cow-report/', sale_cow_report, name='sale_cow_report'),
	path('sale-sale_cow/', sale_cow, name='sale_cow'),


	#path('google/login/callback/', google_login_callback, name='google_login_callback')
]

