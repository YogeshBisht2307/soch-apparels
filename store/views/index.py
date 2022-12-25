from typing import Dict, Optional
from django.http import HttpResponse
from SochApparels.settings import logger
from django.views.generic.base import View
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest

from store.models import Cloth
from store.models import Cart
from store.models import Color
from store.models import Order
from store.models import Brand
from store.models import Comment
from store.models import Payment
from store.models import Occasion
from store.models import Category
from store.models import Order_Item
from store.models import Size_Variant
from store.models import Sub_Category
from store.models import WebsiteDetail


class IndexView(View):
    def _fashion(self, subcat) -> Optional[QuerySet]:
        sub_categories: QuerySet = Sub_Category.objects.all()
        for sub_cat in sub_categories:
            sub_cat.name = (sub_cat.name).title()

        try:
            fashion: Sub_Category = Sub_Category.objects.get(name=subcat)
            return Cloth.objects.filter(sub_category=fashion)
        except:
            return None

    def _valueformoney(self) -> Optional[QuerySet]:
        try:
            return Cloth.objects.filter(cloth_discount__gte=10)
        except:
            return None

    def get(self, request: WSGIRequest) -> HttpResponse:
        web_detail: WebsiteDetail = WebsiteDetail.objects.first()
        new_arrival: str = "New Arrival"
        trending: str = "Trending Fashion"
        context: Dict = {
            'website': web_detail,
            "new_arrival": self._fashion(new_arrival),
            "Trending": self._fashion(trending),
            'valueformoney': self._valueformoney(),
        }
        return render(request, 'store/index.html', context=context)
