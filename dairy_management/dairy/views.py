from django.utils import timezone
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import ProductionRecord, FeedingRecord, ProductionRecordHistory
from .forms import ProductionRecordForm, FeedingRecordForm

from home.models import Sales
from cow.models import Cow
from users.models import User

from django.db.models import Sum
from django.db.models.functions import TruncMonth

from django.contrib import messages
from django.contrib.auth.decorators import login_required

# ProductionRecord Views
@login_required
def list_production_records(request):
	records = ProductionRecord.objects.all()
	cows = Cow.objects.all()
	context = {
		'records': records,
		'cows': cows
	}
	return render(request, 'production/milkcollection.html', context)

@login_required
def detail_production_record(request, cow_id):

	record = get_object_or_404(ProductionRecord, cow__cow_id=cow_id)
	return JsonResponse({
		'production_record': {
		'user': record.user.username,
		'cow': record.cow.name,
		'date': record.date,
		'milk_produced': record.milk_produced
	}})

#Add a milk record
@login_required
def create_production_record(request):
	if request.method == 'POST':
		form = ProductionRecordForm(request.POST)

		if form.is_valid():
			production_record = form.save(commit=False)

			#####Here here here  Use the user who is logged in

			user = User.objects.first()

			production_record.user = user
			production_record.save()
			messages.success(request, 'Record added successfully!')
			return redirect('list_production_records')

		else:
			messages.error(request, 'Error inserting data. Please try again')
	else:
		return JsonResponse({'error': 'GET method not allowed'}, status=405)

#Sum all production record - milk
@login_required
def total_collected_milk(request):
	total_milk = ProductionRecord.objects.aggregate(total=Sum('milk_produced'))['total'] or 0
	return JsonResponse({'total_milk': total_milk})

@login_required
def total_milk_data(request):
	# Total milk sold per month
	milk_sold_monthly = Sales.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_sold=Sum('milk_sold')).values('month', 'total_sold').order_by('month')

	# Format the data for the chart
	monthly_sales_data = [{'month': record['month'].strftime('%B'), 'total_sold': record['total_sold']} for record in milk_sold_monthly]

	return JsonResponse({'monthly_sales_data': monthly_sales_data})

@login_required
def update_production_record(request, id):
	record = get_object_or_404(ProductionRecord, id=id)

	if request.method == 'PUT' or request.method == 'PATCH':
		# Save previous record to history
		ProductionRecordHistory.objects.create(
			production_record=record,
			user=record.user,
			cow=record.cow,
			date=record.date,
			milk_produced=record.milk_produced,
			action='Updated',
				timestamp=timezone.now()
		)


		form = ProductionRecordForm(request.put, instance=id)
		if form.is_valid():
			form.save()
			messages.success(request, 'Production record updated successfully')
		else:
				messages.success(request, 'Something went wrong')

@login_required
def delete_production_record(request, id):
	record = get_object_or_404(ProductionRecord, id=id)

	# Save record to history before deletion
	ProductionRecordHistory.objects.create(
		production_record=record,
		user=record.user,
		cow=record.cow,
		date=record.date,
		milk_produced=record.milk_produced,
		action='Deleted',
				timestamp=timezone.now()

	)

	record.delete()
	return JsonResponse({'message': 'Production record deleted successfully'})






# FeedingRecord Views
@login_required
def list_feeding_records(request):
	records = FeedingRecord.objects.all()
	print('HAaaaaaaaaaalooooooooo')
	context = {
		'records': records
	}
	print(context)
	return render(request, 'production/feed.html', context)



@login_required
def detail_feeding_record(request, id):
	record = get_object_or_404(FeedingRecord, id=id)
	return JsonResponse({'feeding_record': {
		'production_record': record.production_record.id,
		'feed_date': record.feed_date,
		'feed_type': record.feed_type,
		'quantity': record.quantity
	}})

@login_required
def create_feeding_record(request):
	if request.method == 'POST':
		cow_id = request.POST.get('cow_id')
		cow_instance = None
		if cow_id:
			cow_instance = Cow.objects.get(id=cow_id)

		form = FeedingRecordForm(request.POST, cow_instance=cow_instance)
		if form.is_valid():
			form.save()
			return redirect('feed')
		else:
			return JsonResponse({'error': form.errors}, status=400)
	else:
		return JsonResponse("No request")

@login_required
def update_feeding_record(request, id):
	record = get_object_or_404(FeedingRecord, id=id)
	if request.method == 'POST':
		form = FeedingRecordForm(request.POST, instance=record)
		if form.is_valid():
			form.save()
			return JsonResponse({'message': 'Feeding record updated successfully'})
		else:
			return JsonResponse({'errors': form.errors}, status=400)
	return JsonResponse({'error': 'GET method not allowed'}, status=405)

@login_required
def delete_feeding_record(request, id):
	record = get_object_or_404(FeedingRecord, id=id)
	record.delete()
	return JsonResponse({'message': 'Feeding record deleted successfully'})
