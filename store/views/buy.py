from django.shortcuts import render, redirect
from store.models import Cloth, Size_Variant
from django.views.generic.base import View

class BuyView(View):
    def get(self,request):
        cloth_slug = request.GET.get('slug')
        cloth_size = request.GET.get('size')
        buy = request.session.get('buy')
        if buy is None:
            buy = []
        cloth = Cloth.objects.get(cloth_slug=cloth_slug)

        obj = {
            'size': cloth_size,
            'cloth': cloth.id
        }
        buy.append(obj)
        request.session['buy'] =buy
        request.session.save()

        return redirect('Checkout')