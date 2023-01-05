from math import floor
from typing import Dict
from store.models import Cloth
from django.db.models.query import QuerySet
from django.views.generic.base import TemplateView


class ProductDetailView(TemplateView):
    template_name = 'store/product_detail.html'

    def get_context_data(self, **kwargs) -> Dict:
        context: Dict = super().get_context_data(**kwargs)
        cloth_slug: str = kwargs.get('cloth_slug', "")
        self.request.session['buy'] = []

        cloth: Cloth = Cloth.objects.get(cloth_slug=cloth_slug)
        related_cloths: QuerySet = Cloth.objects.filter(sub_category=cloth.sub_category).exclude(cloth_slug=cloth_slug)

        try:
            cloth_size = cloth.size_variant_set.get(size=self.request.GET['size'])
        except KeyError:
            cloth_size = cloth.size_variant_set.all().order_by('price').first()

        price: int = floor(cloth_size.price)
        sale_price: int = floor(price - (price * (cloth.cloth_discount / 100)))
        comments: QuerySet = cloth.comment_set.all().order_by('-date')
        context = {
            'active_size': cloth_size,
            'sale_price': sale_price,
            'price': price,
            "cloth": cloth,
            "related_cloths": related_cloths,
            "comments": comments
        }
        return context

