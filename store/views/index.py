from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Cloth, Size_Variant, Cart, Order, Order_Item, Payment, Occasion, Category, Sub_Category, Color, \
    Brand, Comment, WebsiteDetail
from django.views.generic.base import View


# utility class
class IndexSection():

    # fucntion for new_arrival section
    def Fashion(self,subcat):
        sub_category = Sub_Category.objects.all()
        for s in sub_category:
            s.name = (s.name).title()
        try:
            fashion = Sub_Category.objects.get(name=subcat)
            fashion_cloths = Cloth.objects.filter(sub_category=fashion)
        except:
            fashion_cloths = None
        return fashion_cloths
    # function for value for money section
    def valueformoney(self):
        try:
            vfm_cloths = Cloth.objects.filter(cloth_discount__gte=10)
        except:
            vfm_cloths = None
        return vfm_cloths


# veiw class
class IndexView(View):
    def get(self, request):
        web_detail = WebsiteDetail.objects.first()
        new_arrival = "New Arrival"
        trending = "Trending Fashion"
        context = {
            'website': web_detail,
            "new_arrival": IndexSection.Fashion(self,new_arrival),
            "Trending":IndexSection.Fashion(self,trending),
            'valueformoney': IndexSection.valueformoney(self),
        }
        return render(request, 'store/index.html', context=context)




