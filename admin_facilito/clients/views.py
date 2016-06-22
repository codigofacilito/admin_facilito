from django.contrib.auth.models import User

from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django

from django.contrib.auth.decorators import login_required

from forms import LoginForm
from forms import CreateUserForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import View
from django.views.generic import DetailView


class ShowView(DetailView):
	model = User
	template_name = 'show.html'
	slug_field = 'username'
	slug_url_kwarg = 'username_url'

class ShowUser(TemplateView):
	template_name = "show.html"

class LoginView(View):
	form = LoginForm()
	message = None
	template = 'login.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('client:dashboard')
		return render(request, self.template, self.get_context() )

	def post(self, request, *args, **kwargs):
		username_post = request.POST['username']
		password_post = request.POST['password']
		user = authenticate( username = username_post , password = password_post)
		if user is not None:
			login_django( request, user)
			return redirect('client:dashboard')
		else:
			self.message = "Username o password incorrectos"
		return render(request, self.template, self.get_context() )

	def get_context(self):
		return {'form': self.form, 'message' : self.message}

class DashboardView(LoginRequiredMixin, View):
	login_url = 'client:login'
	def get(self, request, *args, **kwargs):
		return render( request, 'dashboard.html', {})


@login_required( login_url = 'client:login' )
def logout(request):
	logout_django(request)
	return redirect('client:login')


def create(request):
	message = None

	form = CreateUserForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			user = form.save( commit = False )
			user.set_password( user.password )
			user.save()
			return redirect('client:login')
	context = {
		'form' : form
	}
	return render( request, 'create.html', context)













