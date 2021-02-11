from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Cloth, Size_Variant, Order, Order_Item, Payment
from math import floor

from store.forms.checkout_form import CheckoutForm
from django.contrib import messages
import razorpay
from SochApparels.settings import KEY_ID, KEY_SECRET
from django.views.generic.base import View
from django.template import loader
from SochApparels.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


# utility function
def total_payable_amount(cart):
    total = 0
    for c in cart:
        discount = c.get('cloth').cloth_discount
        price = c.get('size').price
        sale_price = floor(price - (price * discount / 100))
        total_of_single_product = sale_price * c['quantity']
        total = total + total_of_single_product
    return total

#preventing duplicated values
def preventing_duplicate(buy):
    length = len(buy)
    if length > 1:
        for i in range(length - 1):
            buy.pop()


class CheckoutView(View):
    def get(self,request):
        form = CheckoutForm()
        buy = request.session.get('buy')
        cart = request.session.get('cart')
        if buy is None:
            buy = []
        if cart is None:
            cart = []
        #iterating over cart
        for c in cart:
            size_str = c.get('size')
            cloth_id = c.get('cloth')
            cloth_obj = Size_Variant.objects.get(size=size_str, cloth=cloth_id)
            c['size'] = cloth_obj
            c['cloth'] = cloth_obj.cloth

        #iterating over buy
        for b in buy:
            cloth_id = b.get('cloth')
            cloth_size = b.get('size')
            cloth_obj = Size_Variant.objects.get(size=cloth_size, cloth=cloth_id)
            b['size']= cloth_obj
            b['cloth']=cloth_obj.cloth
            b['total'] = cloth_obj.price

        #preventing duplicated value in buy
        preventing_duplicate(buy)

        context={
            'form': form,
            'cart': cart,
            'buy' :buy,
            }
        return render(request, 'store/checkout.html', context=context)

    def post(self,request):
        user = None
        form = CheckoutForm(request.POST)
        if request.user.is_authenticated:
            user = request.user

        if form.is_valid():
            buy = request.session.get('buy')
            cart = request.session.get('cart')

            #creating order
            shipping_address = form.cleaned_data.get('shipping_address')
            phone = form.cleaned_data.get('phone')
            payment_method = form.cleaned_data.get('payment_method')
            order = Order()
            order.shipping_address = shipping_address
            order.phone = phone
            order.payment_method = payment_method

            #logic for buing item directly through pay button
            if buy:
                price = 0
                for b in buy:
                    size_str = b.get('size')
                    cloth_id = b.get('cloth')
                    cloth_obj = Size_Variant.objects.get(size=size_str, cloth=cloth_id)
                    cloth = Cloth.objects.get(id = cloth_id)
                    b['size'] = cloth_obj
                    b['cloth'] = cloth_obj.cloth
                    price = cloth_obj.price
                    price =  floor(price - (price * (cloth.cloth_discount / 100)))
                    b['total']= price

                order.total = price

                order.order_status = "PENDING"
                order.user = user
                order.save()
                # preventing duplicated value in buy
                preventing_duplicate(buy)

                #creating order item
                for b in buy:
                    order_item = Order_Item()
                    order_item.order = order
                    size = b.get('size')
                    cloth = b.get('cloth')
                    order_item.price = floor(size.price - (size.price * (cloth.cloth_discount / 100)))
                    order_item.quantity = 1
                    order_item.size = size
                    order_item.cloth = cloth
                    order_item.save()

        #logic for buying item through cart
            else:
                if cart is None:
                    cart = []
                for c in cart:
                    size_str = c.get('size')
                    cloth_id = c.get('cloth')
                    cloth_obj = Size_Variant.objects.get(size=size_str, cloth=cloth_id)
                    c['size'] = cloth_obj
                    c['cloth'] = cloth_obj.cloth
                total = total_payable_amount(cart)
                order.total = total
                order.order_status = "PENDING"
                order.user = user
                order.save()

                # saving order items
                for c in cart:
                    order_item = Order_Item()
                    order_item.order = order
                    size = c.get('size')
                    cloth = c.get('cloth')
                    order_item.price = floor(size.price - (size.price * (cloth.cloth_discount / 100)))
                    order_item.quantity = c.get('quantity')
                    order_item.size = size
                    order_item.cloth = cloth
                    order_item.save()

            if payment_method=="ONLINE":
                # creating payment
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

                payment = Payment()
                payment.order = order
                payment.payment_request_id = payment_id['id']
                payment.save()
                form = CheckoutForm()
                context = {
                    'form': form,
                    'cart': cart,
                    'buy': buy,
                    'payment': payment_id
                }
                return render(request, 'store/checkout.html', context=context)
            else:
                order.order_status = "PLACED"
                order.save()
                try:
                    context = {
                        "username": user.first_name,
                        "order": order,
                    }

                    html_message = loader.render_to_string("store/product_email.html", context=context)

                    # mail to coustomer
                    send_mail(
                        'Product Purchased',
                        'Payment for ordered product has successfull worth of money !',
                        EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                        html_message=html_message,
                    )
                    # mail to user
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
        else:
            return redirect('/checkout/')
