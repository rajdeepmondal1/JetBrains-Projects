from django.shortcuts import render
from django.views import View
from .models import Resume


class Resumes(View):
    def get(self, request, *args, **kwargs):
        resume = Resume.objects.all()
        return render(request, 'resumes.html', context={'resumes': resume})