from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from home.models import Sales
from cow.models import Cow
from dairy.models import ProductionRecord
from users.models import User
from django.db.models import Sum
from .forms import SalesForm

from django.contrib import messages


from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount


# Create your views here.
def custom_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		print(f"Username: {username}")
		print(f"Password: {password}")

		authenticated_user = authenticate(request, username=username, password=password)
				
		print(f"Authenticated User: {authenticated_user}")

		if authenticated_user is not None:
			login(request, authenticated_user)
			messages.success(request, 'Logged in')
			return redirect('dashboard_view')
		else:
			messages.error(request, 'Invalid credentials. Please try again.')
			return redirect('login')
	else:
		return render(request, 'index.html')


def home(request):
	return render(request, 'index.html')

@login_required
def dashboard(request):
	return render(request, 'production/dashboard.html')


@login_required
def cows(request):
	return render(request, 'production/cowinfo.html')

@login_required
def staffinfo(request):
	staffs = User.objects.all() 
	context = {
		'staffs': staffs
	}  
	return render(request, 'production/staffinfo.html', context)

@login_required
def vaccine_page(request):
	return render(request, 'production/vaccine.html')

@login_required
def sale_milk_report(request):
	return render(request, 'production/salemilkreport.html')

@login_required
def sale_cow_report(request):
	return render(request, 'production/salecowreport.html')

@login_required
def sale_cow(request):
	return render(request, 'production/salecow.html')


@login_required
def sale_milk(request):
	cows = ProductionRecord.objects.all()
	context = {
		'cows': cows
	}
	return render(request, 'production/salemilk.html', context)

@login_required
def dashboard_view(request):
		#fetch all cows
		cows = Cow.objects.all()
		no_of_cows = cows.count()

		#fetch total collected milk
		total_milk = ProductionRecord.objects.aggregate(total=Sum('milk_produced'))['total'] or 0
		total_sold_milk = Sales.objects.aggregate(total=Sum('liter'))['total'] or 0
		total_staff = User.objects.filter().count()

		#context to pass to template
		context = {
			'total_staff': total_staff,
			'no_of_cows': no_of_cows,
			'total_milk': total_milk,
			'total_sold_milk': total_sold_milk,
		}
		return render(request, 'production/dashboard.html', context)

@login_required
def create_sales(request):
		if request.method == 'POST':
				form = SalesForm(request.POST)
				if form.is_valid():
						form.save()
						messages.success(request, 'Sale added successfully!')
						#return redirect('sale_milk') 
						return JsonResponse({'message': 'Cow added successfully'}, status=200)

				else:
						messages.error(request, 'Something went wrong, please try again!')
		else:
			return JsonResponse("Not a post request")	
