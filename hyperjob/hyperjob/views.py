from django.shortcuts import render
from django.views import View
from resume.models import Resume
from vacancy.models import Vacancy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .forms import AddForm


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main.html')


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signup.html'


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'home.html')
        else:
            return HttpResponseRedirect('/login')


class NewResumeView(View):
    def post(self, request, *args, **kwargs):
        form = AddForm(request.POST)
        if form.is_valid():
            clean_form = form.cleaned_data
            description = clean_form['description']
            if request.user.is_authenticated and not request.user.is_staff:
                resume = Resume(description=description, author=request.user)
                resume.save()
                return HttpResponseRedirect('/home')
            else:
                return HttpResponseForbidden()
        return HttpResponseForbidden()


class NewVacancyView(View):
    def post(self, request, *args, **kwargs):
        form = AddForm(request.POST)
        if form.is_valid():
            clean_form = form.cleaned_data
            description = clean_form['description']
            if request.user.is_authenticated and request.user.is_staff:
                vacancy = Vacancy(description=description, author=request.user)
                vacancy.save()
                return HttpResponseRedirect('/home')
            else:
                return HttpResponseForbidden()
        return HttpResponseForbidden()
