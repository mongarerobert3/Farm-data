import json
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Cow
from .forms import CowForm, VaccinateForm

from django.contrib.auth.decorators import login_required

from django.contrib import messages

#create a cow
@login_required
def create_cow(request):
	if request.method == 'POST':
		
		form = CowForm(request.POST) #request.FILES - for image
		if form.is_valid():
			form.save()
			messages.success(request, 'Cow added successfully!')
			return redirect('all_cows')
		else:
			messages.error(request, 'Error inserting data. Please try again')
	
		return JsonResponse({'error': 'GET method not allowed'}, status=405)


#get cows
@login_required
def all_cows(request):
	cows = Cow.objects.all()
	context = {
		'cows': cows
	}
	return render(request, 'production/cowinfo.html', context)

#get a cow
@login_required
def search_cow(request, name=None):
	if name:
		cow = get_object_or_404(Cow, name=name)
		return render(request, 'cow/cow_detail.html', {'cow': cow})
	else:
		return render(request, 'cow/cow_detail.html', {'error_message': 'Please provide Cow Name'})

#update cow
@login_required
def update_cow(request, name):
	cow = get_object_or_404(Cow, name=name)
	if request.method == 'POST':
		form = CowForm(request.POST, instance=cow)
		if form.is_valid():
			form.save()
			return redirect('all_cows')
	else:
		form = CowForm(instance=cow)
	return render(request, 'cow/cow_form.html', {'form':form})

#delete a cow
@login_required
def delete_cow(request, cow_id):
    cow = get_object_or_404(Cow, cow_id=cow_id)
    if request.method == 'POST':
        cow.delete()
        messages.success(request, 'Cow deleted successfully')
        return redirect('all_cows')
    return HttpResponse('Cow deleted successfully')



#cow vaccination
@login_required
def vaccinate_cow(request, cow_id):
	cow = get_object_or_404(Cow, cow_id=cow_id)

	if request.method == 'POST':
		try:
			data = json.loads(request.body)
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Invalid JSON'}, status=400)

		form = VaccinateForm(data)
		if form.is_valid():
			vaccination = form.save(commit=False)
			vaccination.cow_vaccinated = cow
			vaccination.save()
			return JsonResponse({'message': 'Vaccination record added successfully'})
		else:
			return JsonResponse({'errors': form.errors}, status=400)
	
	return JsonResponse({'message': 'Bad Request'}, status=400)
