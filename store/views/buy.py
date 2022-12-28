from typing import Dict, List
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from django.core.handlers.wsgi import WSGIRequest
from store.models import Cloth, Size_Variant


class BuyView(View):
    def get(self, request: WSGIRequest) -> response.HttpResponseRedirect:
        cloth_slug: str = request.GET.get('slug', "")
        cloth_size: str = request.GET.get('size', "")
        buy: List = request.session.get('buy', [])

        cloth: Cloth = Cloth.objects.get(cloth_slug=cloth_slug)
        buy.append({'size': cloth_size, 'cloth': cloth.id})
        request.session['buy'] =buy
        request.session.save()
        return redirect('Checkout')