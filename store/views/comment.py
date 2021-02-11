from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Cloth, Size_Variant,Cart, Order, Order_Item, Payment, Occasion, Category,Sub_Category,Color,Brand, Comment
from math import floor
from django.contrib.auth.decorators import login_required
from store.forms.authforms import CustomerCreationForm,CustomerAuthenticationForm #imporing the class from froms folder
from django.contrib.auth import authenticate, login as loginUser
from django.views.generic.base import View


class CommentView(View):
    def post(self,request):
        comment = request.POST.get('comment')
        return_url = request.POST.get('return_url')
        cloth_slug = request.POST.get('cloth_slug')
        cloth = Cloth.objects.get(cloth_slug=cloth_slug)
        if comment != "" and len(comment) > 4:
            user = request.user
            comments = Comment()
            comments.comment = comment
            comments.user = user
            comments.cloth = cloth
            comments.save()

        return redirect(return_url)
