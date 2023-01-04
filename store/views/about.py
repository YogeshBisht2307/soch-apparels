from typing import Dict
from store.models.about import About
from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest


class AboutView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        about: About = About.objects.all().first()
        context: Dict ={
            'about':about,
        }
        return render(request, 'store/about.html',context=context)