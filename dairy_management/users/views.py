# users/views.py
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.models import User
from .forms import UserForm,DoctorForm

import logging
logger = logging.getLogger(__name__)


@login_required
def add_doctor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        form = DoctorForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Doctor added successfully'})
        return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully!')
            return redirect('staff')
        else:
            #errors = form.errors.as_json() 
            if 'username' in form.errors:
                messages.error(request, 'Email already exists. Please choose a different email.')
            else:
                messages.error(request, 'Failed to add user. Please check the form.')            
                return redirect('staff')
            return redirect('dashboard_view')

@login_required
def all_admins(request):
    admins = User.objects.filter(is_staff=False) 
    admin_list = list(admins.values())  
    return JsonResponse(admin_list, safe=False)

@login_required
def update_user(request, id):
    if request.method != 'POST':
        return JsonResponse({'message':'Invalid request method'}, status=405)
    
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse ({'message': 'Invalid json'}, status=400)

    if 'email' in data:
        user.email = data['email']
    if 'name' in data:
        user.name = data['name']
    if 'phone' in data:
        user.phone = data['phone']
    if 'password' in data:
        user.set_password(data['password'])
    if 'is_staff' in data:
        user.is_staff = bool(data['is_staff'])
    
    try:
        user.save()
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)
    
    return JsonResponse({'message': 'User updated successfully'})


#delete a user
@login_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('staff')
    return HttpResponse('User deleted successfully')