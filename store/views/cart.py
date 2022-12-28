from typing import List, Dict
from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from django.core.handlers.wsgi import WSGIRequest
from store.models import Cloth, Size_Variant, Cart
from django.views.generic.base import View, TemplateView


class AddCartView(View):
    def get(self, request: WSGIRequest, cloth_slug: str, size: str) -> response.HttpResponseRedirect:
        user = request.user if request.user.is_authenticated else None
        cart: List  = request.session.get('cart', [])

        #TODO: Run queries asynchrousely
        cloth: Cloth = Cloth.objects.get(cloth_slug=cloth_slug)
        size_temp: Size_Variant = Size_Variant.objects.get(size=size, cloth=cloth)

        in_cart: bool = False
        for cart_obj in cart:
            if cart_obj.get('cloth') != cloth.id or cart_obj.get('size') != size:
                continue

            cart_obj['quantity'] = cart_obj['quantity'] + 1
            in_cart = True

        if not in_cart:
            cart_obj = {
                'cloth': cloth.id,
                'size': size,
                'quantity': 1
            }
            cart.append(cart_obj)
        
        return_url = request.GET.get('return_url')
        request.session['cart'] = cart
        if not user:
            return redirect(return_url)

        existing = Cart.objects.filter(user=user, sizeVariant=size_temp)
        if len(existing) > 0:
            obj = existing[0]
            obj.quantity = obj.quantity + 1
            obj.save()
        else:
            cart_obj = Cart()
            cart_obj.user = user
            cart_obj.sizeVariant = size_temp
            cart_obj.quantity = 1
            cart_obj.save()
        return redirect(return_url)


class CartView(TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', [])

        # TODO: Fetch all cart related data in single query for cloth instead of inside loop
        for cart_obj in cart:
            cloth_id = cart_obj.get('cloth', "")
            cloth = Cloth.objects.get(id=cloth_id)
            cart_obj['size'] = Size_Variant.objects.get(cloth=cloth_id, size=cart_obj['size'])
            cart_obj['cloth'] = cloth

        context = {'cart': cart}
        return context


class RemoveCartView(View):
    """
        This function remove the cloth item from the cart :- 
        1. If user not logged in it will just update the anonymouos user session.s
        2. If user is logged in it will remove the cloth entry from database and user session.
    """
    def get(self, request: WSGIRequest, cloth_slug: str, size: str) -> response.HttpResponseRedirect:
        user = request.user if request.user.is_authenticated else None
        cart: List = request.session.get('cart', [])

        cloth: Cloth = Cloth.objects.get(cloth_slug=cloth_slug)
        size_var: Size_Variant = Size_Variant.objects.get(size=size, cloth=cloth)
        if user:
            obj = Cart.objects.filter(user=user, sizeVariant=size_var)
            obj.delete()

        for cart_obj in range(len(cart)):
            if cart[cart_obj]['cloth'] != cloth.id or cart[cart_obj]['size'] != size:
                continue
            del cart[cart_obj]
            break

        request.session['cart'] = cart
        return_url = request.GET.get('return_url')
        return redirect(return_url)
