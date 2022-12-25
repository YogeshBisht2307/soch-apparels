from typing import Dict, List
from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login as loginUser

from store.models import Size_Variant, Cart
from store.forms.authforms import CustomerCreationForm
from store.forms.authforms import CustomerAuthenticationForm


class RegistrationView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        form: CustomerCreationForm = CustomerCreationForm()
        context: Dict = {
            "form": form
        }
        return render(request, 'store/registration.html', context=context)

    def post(self, request: WSGIRequest) -> HttpResponse:
        form: CustomerCreationForm = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
            return redirect('login')

        context: Dict = {
            "form": form
        }
        return render(request, 'store/registration.html', context=context)


class LoginView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        next_page: str = request.GET.get('next')
        if next_page:
            request.session['next_page'] = next_page

        form: CustomerAuthenticationForm = CustomerAuthenticationForm()
        context = {
            "form": form
        }
        return render(request, 'store/login.html', context=context)

    def post(self, request: WSGIRequest) -> HttpResponse:
        form: CustomerAuthenticationForm = CustomerAuthenticationForm(data=request.POST)
        if not form.is_valid():
            context: Dict = {
                "form": form
            }
            return render(request, 'store/login.html', context=context)

        username: str = form.cleaned_data.get("username")
        password: str = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return

        loginUser(request, user)
        session_cart: List = request.session.get('cart')
        if session_cart:
            for c in session_cart:
                size: str = c.get('size')
                quantity: str = c.get('quantity')
                cloth_id: str = c.get('cloth')
                cart_obj: Cart = Cart()
                cart_obj.sizeVariant = Size_Variant.objects.get(size=size, cloth=cloth_id)
                cart_obj.quantity = quantity
                cart_obj.user = user
                cart_obj.save()

        cart: Cart = Cart.objects.filter(user=user)
        session_cart = []
        for c in cart:
            obj: Dict = {
                'size': c.sizeVariant.size,
                'cloth': c.sizeVariant.cloth.id,
                'quantity': c.quantity

            }
            session_cart.append(obj)

        request.session['cart'] = session_cart
        next_page: str = request.session.get('next_page')
        if not next_page:
            next_page = "Home"
        if user.is_staff:
            next_page = "/admin"
        return redirect(next_page)


class LogoutView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        request.session.clear()
        return redirect('Login')

