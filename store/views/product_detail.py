from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Cloth

from math import floor
from django.views.generic.base import TemplateView


class ProductDetailView(TemplateView):
    template_name = 'store/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cloth_slug = kwargs.get('cloth_slug')
        request = self.request
        buy = []
        request.session['buy'] = buy
        cloth = Cloth.objects.get(cloth_slug=cloth_slug)
        related_cloths = Cloth.objects.filter(sub_category=cloth.sub_category).exclude(cloth_slug=cloth_slug)
        size = request.GET.get('size')
        if size == None:
            size = cloth.size_variant_set.all().order_by('price').first()
        else:
            size = cloth.size_variant_set.get(size=size)
        price = floor(size.price)
        sale_price = floor(price - (price * (cloth.cloth_discount / 100)))
        comments = cloth.comment_set.all().order_by('-date')
        context = {
            'active_size': size,
            'sale_price': sale_price,
            'price': price,
            "cloth": cloth,
            "related_cloths": related_cloths,
            "comments": comments
        }
        return context

