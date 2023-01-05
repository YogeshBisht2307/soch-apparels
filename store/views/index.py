from typing import Dict, Optional
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.db.models.query import QuerySet
from django.core.handlers.wsgi import WSGIRequest

from store.models import Cloth
from store.models import Sub_Category
from store.models import WebsiteDetail


class IndexView(View):
    def _fashion(self, subcat) -> Optional[QuerySet]:
        sub_categories: QuerySet = Sub_Category.objects.all()
        for sub_cat in sub_categories:
            sub_cat.name = (sub_cat.name).title()

        fashion: Sub_Category = Sub_Category.objects.get(name=subcat)
        return Cloth.objects.filter(sub_category=fashion)

    def _valueformoney(self) -> Optional[QuerySet]:
        return Cloth.objects.filter(cloth_discount__gte=10)

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
