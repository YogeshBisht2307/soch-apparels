from django.views.generic.base import View
from django.shortcuts import render, redirect
from store.models.about import About

class AboutView(View):
    def get(self, request):
        about = About.objects.all().first()
        context={
            'about':about,
        }
        return render(request, 'store/about.html',context=context)