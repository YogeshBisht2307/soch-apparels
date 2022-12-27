from typing import Dict, List

from urllib.parse import urlencode
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.paginator import Page
from django.http.request import QueryDict
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

from store.models import Cloth
from store.models import Occasion
from store.models import Category
from store.models import Sub_Category
from store.models import Color
from store.models import Brand


class StoreView(TemplateView):
    template_name = 'store/shop.html'

    def get_context_data(self, **kwargs) -> Dict:
        context: Dict = super().get_context_data(**kwargs)
        query: QueryDict = self.request.GET

        category = query.get('category')
        sub_category = query.get('sub_category')
        occasion = query.get('occasion')
        brand = query.get('brand')
        color = query.get('color')
        page = query.get('page')

        page = 1 if not page else page

        query_parameter: Dict = {}
        query_parameter.update({'category__slug': category}) if category else None
        query_parameter.update({'sub_category__slug': sub_category}) if sub_category else None
        query_parameter.update({'ocassion__slug': occasion}) if occasion else None
        query_parameter.update({'brand__slug': brand}) if brand else None
        query_parameter.update({'color__slug': color}) if color else None

        # TODO: Run these query in parllel (async)
        cloths: QuerySet = Cloth.objects.filter(**query_parameter).order_by('-created')
        occasions: QuerySet = Occasion.objects.all()
        brands: QuerySet = Brand.objects.all()
        colors: QuerySet = Color.objects.all()
        categories: QuerySet = Category.objects.all()
        sub_categories: QuerySet = Sub_Category.objects.all()

        paginator: Paginator = Paginator(cloths, 9)
        page_object: Page = paginator.get_page(page)

        query = self.request.GET.copy()
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
        cart = self.request.session.get('cart')
        return context
