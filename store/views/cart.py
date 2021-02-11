from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Cloth, Size_Variant, Cart
from django.views.generic.base import View, TemplateView


class AddCartView(View):
    def get(self, request, cloth_slug, size):
        user = None
        if request.user.is_authenticated:
            user = request.user
        cart = request.session.get('cart')
        if cart is None:
            cart = []

        cloth = Cloth.objects.get(cloth_slug=cloth_slug)
        size_temp = Size_Variant.objects.get(size=size, cloth=cloth)

        flag = True
        for cart_obj in cart:
            c_id = cart_obj.get('cloth')
            size_short = cart_obj.get('size')
            if c_id == cloth.id and size == size_short:
                cart_obj['quantity'] = cart_obj['quantity'] + 1
                flag = False

        if flag:
            cart_obj = {
                'cloth': cloth.id,
                'size': size,
                'quantity': 1
            }
            cart.append(cart_obj)

        if user != None:
            existing = Cart.objects.filter(user=user, sizeVariant=size_temp)
            if len(existing) > 0:
                obj = existing[0]
                obj.quantity = obj.quantity + 1
                obj.save()
            else:
                c = Cart()
                c.user = user
                c.sizeVariant = size_temp
                c.quantity = 1
                c.save()
        request.session['cart'] = cart
        return_url = request.GET.get('return_url')
        return redirect(return_url)


class CartView(TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        cart = request.session.get('cart')
        if cart is None:
            cart = []
        for c in cart:
            cloth_id = c.get('cloth')
            cloth = Cloth.objects.get(id=cloth_id)
            c['size'] = Size_Variant.objects.get(cloth=cloth_id, size=c['size'])
            c['cloth'] = cloth

        context = {
            'cart': cart
        }
        return context


class RemoveCartView(View):
    def get(self, request, cloth_slug, size):
        user = None
        cloth = Cloth.objects.get(cloth_slug=cloth_slug)
        cart = request.session.get('cart')
        size_var = Size_Variant.objects.get(size=size, cloth=cloth)
        if request.user.is_authenticated:
            user = request.user
        if user != None:
            obj = Cart.objects.filter(user=user, sizeVariant=size_var)
            obj.delete()

        for cart_obj in range(len(cart)):
            if cart[cart_obj]['cloth'] == cloth.id and cart[cart_obj]['size'] == size:
                del cart[cart_obj]
                break

        request.session['cart'] = cart

        return_url = request.GET.get('return_url')
        return redirect(return_url)
