from urllib import request
from django.shortcuts import render
#import predictions

# Create your views here.
def predict(request):
	return render(request, 'production/predictions.html')