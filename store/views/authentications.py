from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Size_Variant, Cart
# imporing the class from froms folder
from store.forms.authforms import CustomerCreationForm,CustomerAuthenticationForm
from django.contrib.auth import authenticate, login as loginUser
from django.views.generic.base import View


class RegistrationView(View):
    def get(self, request):
        form = CustomerCreationForm()  # calling the forms class
        context = {
            "form": form
        }
        return render(request, 'store/registration.html', context=context)

    def post(self, request):
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
            return redirect('login')
        context = {
            "form": form
        }
        return render(request, 'store/registration.html', context=context)


class LoginView(View):
    def get(self, request):
        next_page = request.GET.get('next')
        if next_page is not None:
            request.session['next_page'] = next_page
        form = CustomerAuthenticationForm()
        context = {
            "form": form
        }
        return render(request, 'store/login.html', context=context)

    def post(self, request):
        form = CustomerAuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)  # authenticating user weather its or not
            if user:
                loginUser(request, user)  # adding user in session
                session_cart = request.session.get('cart')
                if session_cart is None:
                    session_cart = []
                else:
                    for c in session_cart:
                        size = c.get('size')
                        quantity = c.get('quantity')
                        cloth_id = c.get('cloth')
                        cart_obj = Cart()
                        cart_obj.sizeVariant = Size_Variant.objects.get(size=size, cloth=cloth_id)
                        cart_obj.quantity = quantity
                        cart_obj.user = user
                        cart_obj.save()

                cart = Cart.objects.filter(user=user)
                session_cart = []
                for c in cart:
                    obj = {
                        'size': c.sizeVariant.size,
                        'cloth': c.sizeVariant.cloth.id,
                        'quantity': c.quantity

                    }
                    session_cart.append(obj)
                request.session['cart'] = session_cart
                next_page = request.session.get('next_page')
                if next_page is None:
                    next_page = "home"
                return redirect(next_page)
        else:
            context = {
                "form": form
            }
            return render(request, 'store/login.html', context=context)


class LogoutView(View):
    def get(self, request):
        request.session.clear()
        return redirect('login')

