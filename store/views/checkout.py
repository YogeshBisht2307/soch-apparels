import razorpay
from math import floor
from typing import Dict, List

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from django.core.handlers.wsgi import WSGIRequest
from store.models import Cloth, Size_Variant, Order, Order_Item, Payment

from django.template import loader
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic.base import View
from store.forms.checkout_form import CheckoutForm
from SochApparels.settings import KEY_ID, KEY_SECRET
from SochApparels.settings import EMAIL_HOST_USER


class CheckoutView(View):
    def _total_payable_amount(self, cart: List) -> int:
        total: int = 0
        for cart_obj in cart:
            discount: int = cart_obj['cloth'].cloth_discount
            price: int = cart_obj['size'].price

            sale_price: int = floor(price - (price * discount / 100))
            total_of_single_product: int = sale_price * cart_obj['quantity']
            total = total + total_of_single_product

        return total

    def get(self, request: WSGIRequest) -> HttpResponse:
        form = CheckoutForm()
        buy: List = request.session.get('buy', [])
        cart: List = request.session.get('cart', [])

        for cart_obj in cart:
            try:
                size_obj: Size_Variant = Size_Variant.objects.get(
                    size=cart_obj['size'], cloth=cart_obj['cloth']
                )
                if not size_obj:
                    continue
            except KeyError:
                continue

            cart_obj['size'] = size_obj
            cart_obj['cloth'] = size_obj.cloth

        for buy_obj in buy:
            try:
                size_obj = Size_Variant.objects.get(
                    size=buy_obj['size'], cloth=buy_obj['cloth']
                )
                if not size_obj:
                    continue
            except KeyError:
                continue
    
            buy_obj['size'] = size_obj
            buy_obj['cloth'] = size_obj.cloth
            buy_obj['total'] = size_obj.price

        context: Dict = {
            'form': form,
            'cart': cart,
            'buy' : buy[:1],
        }
        return render(request, 'store/checkout.html', context=context)

    def post(self, request: WSGIRequest) -> response.HttpResponseRedirect:
        form: CheckoutForm = CheckoutForm(request.POST)
        user = request.user if request.user.is_authenticated else None
        buy: List = request.session.get('buy', [])
        cart: List = request.session.get('cart', [])
        print(cart)

        if not form.is_valid():
            return redirect('/checkout/')

        shipping_address = form.cleaned_data.get('shipping_address', "")
        phone = form.cleaned_data.get('phone')
        payment_method = form.cleaned_data.get('payment_method')
        order = Order(shipping_address=shipping_address, phone=phone, payment_method=payment_method)

        if not buy:
            for cart_obj in cart:
                try:
                    cloth_obj = Size_Variant.objects.get(
                        size=cart_obj['size'], cloth=cart_obj['cloth']
                    )
                except KeyError:
                    continue

                cart_obj['size'] = cloth_obj
                cart_obj['cloth'] = cloth_obj.cloth

            total = self._total_payable_amount(cart)
            order.total = total
            order.order_status = "PENDING"
            order.user = user
            order.save()

            for cart_obj in cart:
                order_item = Order_Item()
                order_item.order = order

                try:
                    size = cart_obj['size']
                    cloth = cart_obj['cloth']
                    order_item.price = floor(
                        size.price - (size.price * (cloth.cloth_discount / 100))
                    )
                    order_item.quantity = cart_obj['quantity']
                except KeyError:
                    continue

                order_item.size = size
                order_item.cloth = cloth
                order_item.save()


        for buy_obj in buy[:1]:
            try:
                size_str: str = buy_obj['size']
                cloth_id: str = buy_obj['cloth']
            except KeyError:
                continue

            size_obj = Size_Variant.objects.get(size=size_str, cloth=cloth_id)
            cloth = Cloth.objects.get(id=cloth_id)
            buy_obj['size'] = size_obj
            buy_obj['cloth'] = size_obj.cloth
            price =  floor(size_obj.price - (size_obj.price * (cloth.cloth_discount / 100)))
            buy_obj['total']= price
            order.total = price
            order.order_status = "PENDING"
            order.user = user
            order.save()

        for buy_obj in buy:
            order_item = Order_Item()
            order_item.order = order
            try:
                size = buy_obj['size']
                cloth = buy_obj['cloth']
            except KeyError:
                continue
    
            order_item.price = floor(size.price - (size.price * (cloth.cloth_discount / 100)))
            order_item.quantity = 1
            order_item.size = size
            order_item.cloth = cloth
            order_item.save()

        if payment_method == "ONLINE":
            try:
                client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
                payment_id = client.order.create(
                    {
                        "amount": order.total * 100,
                        'currency': 'INR',
                        'payment_capture': '1',
                    }
                )
            except:
                messages.error(request, 'Payment gateway is not Responding , Check your connection !')
                return redirect('Checkout')

            payment: Payment = Payment()
            payment.order = order
            payment.payment_request_id = payment_id['id']
            payment.save()
            checkout_form: CheckoutForm = CheckoutForm()
            context: Dict = {
                'form': checkout_form,
                'cart': cart,
                'buy': buy,
                'payment': payment_id,
                'rz_key': KEY_ID
            }
            return render(request, 'store/checkout.html', context=context)
        else:
            order.order_status = "PLACED"
            order.save()
            request.session['cart'] = [] if not buy else cart 
            request.session['buy'] = []
            try:
                context = {
                    "username": user.first_name,
                    "order": order,
                }

                html_message = loader.render_to_string("store/product_email.html", context=context)

                send_mail(
                    'Product Purchased',
                    'Payment for ordered product has successfull!',
                    EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                    html_message=html_message,
                )

                send_mail(
                    'Product Purchased',
                    f"You have recieved a COD delivery order of {order.total} Rupee for order id = {order.id}, check it out and procced for delivery",
                    EMAIL_HOST_USER,
                    [EMAIL_HOST_USER],
                    fail_silently=False,
                )
            except:
                return redirect('Orders')

            return redirect('Orders')