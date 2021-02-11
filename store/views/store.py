from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Cloth, Occasion, Category, Sub_Category, Color,Brand
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django.views.generic.base import TemplateView

class StoreView(TemplateView):
    template_name = 'store/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        query = request.GET
        cloths = []
        cloths = Cloth.objects.all()
        category = query.get('category')
        sub_category = query.get('sub_category')
        occasion = query.get('occasion')
        brand = query.get('brand')
        color = query.get('color')
        page = query.get('page')

        if page is None and page == "":
            page = 1

        if category != "" and category is not None:
            cloths = cloths.filter(category__slug=category)
        if sub_category != "" and sub_category is not None:
            cloths = cloths.filter(sub_category__slug=sub_category)
        if occasion != "" and occasion is not None:
            cloths = cloths.filter(ocassion__slug=occasion)
        if brand != "" and brand is not None:
            cloths = cloths.filter(brand__slug=brand)
        if color != "" and color is not None:
            cloths = cloths.filter(color__slug=color)

        occasions = Occasion.objects.all()
        brands = Brand.objects.all()
        colors = Color.objects.all()
        categories = Category.objects.all()
        sub_categories = Sub_Category.objects.all()

        paginator = Paginator(cloths, 9)
        page_object = paginator.get_page(page)

        query = request.GET.copy()
        query['page'] = ''
        pageurl = urlencode(query)

        context = {
            "page_object": page_object,
            "occassions": occasions,
            "brands": brands,
            "colors": colors,
            "categories": categories,
            "sub_categories": sub_categories,
            'pageurl': pageurl
        }
        cart = request.session.get('cart')
        return context

