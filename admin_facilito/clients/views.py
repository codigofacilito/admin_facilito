from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from forms import LoginForm
from forms import CreateUserForm


#decoradores
def user_authenticated(user):
	return not user.is_authenticated()

# Create your views here.
def show(request):
	return HttpResponse("Hola Mundo desde el cliente")

@user_passes_test(user_authenticated, login_url = 'client:dashboard')
def login(request):
	message = None
	if request.method == 'POST':#se envio el formulario
		username_post = request.POST['username']
		password_post = request.POST['password']
		user = authenticate( username = username_post, password = password_post)
		if user is not None:
			login_django(request, user)
			return redirect('client:dashboard')
		else:
			message = 'Username o password incorrectos'

	form = LoginForm()
	context = {
		'form' : form,
		'message' : message
	}
	return render( request, 'login.html', context )

@login_required(login_url = 'client:login')
def dashboard(request):
	username = request.user.username
	return render( request, 'dashboard.html', {'username' : username} )	

def logout(request):
	logout_django(request)
	return redirect('client:login')


def create(request):
	message = None

	form = CreateUserForm(request.POST or None)
	if request.method =='POST':
		if form.is_valid():
			user = form.save( commit = False )
			password = user.password #Este en texto plano
			user.set_password(password)
			user.save()
			return redirect('client:login')
		else:
			message = "Formulario no valido"

	context = {
		'form':  form,
		'message' : message
	}
	return render( request, 'create.html', context )









