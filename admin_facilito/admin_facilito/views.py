from django.shortcuts import render

def home(reques):
	return render(reques, 'home.html', {})