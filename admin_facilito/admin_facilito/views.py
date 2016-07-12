from django.shortcuts import render

def home(request):
	return render(request, 'home.html', {})

def error_404(request):
	return render(request, 'error_404.html', {})	