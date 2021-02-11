from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Cloth, Size_Variant, Cart, Order, Order_Item, Payment, Occasion, Category, Sub_Category, Color, \
    Brand, Comment
from math import floor

from store.forms.authforms import CustomerCreationForm, \
    CustomerAuthenticationForm  # imporing the class from froms folder
from django.contrib.auth import authenticate, login as loginUser
from django.core.paginator import Paginator
from django.views.generic.base import View
from django.contrib import messages
from django.core.mail import send_mail
from SochApparels.settings import EMAIL_HOST_USER


class CancelOrderView(View):
    def get(self, request):
        user = request.user
        # getting the value of order_id
        order_id = request.GET.get('oddl')
        order = Order.objects.get(id=order_id)
        if order.order_status != "CANCELED" and order.order_status != "COMPLETE":
            order.order_status = "CANCELED"
            order.save()
            send_mail("Order Cancellation request !",
                      f"You have recieved a request for order cancelattion from {user.email} , Mobile Number==> {order.phone} of Price ==> {order.total}.... and order id is:- {order_id} ==> Procced for the cancellation process",
                      'Yogeshbisht.2307@gmail.com', [EMAIL_HOST_USER])
            messages.success(request,
                             f'Your order has cancelled, 10% from price will be conduct for cancellation charges and , money will be return within 2 working days...!')
            return redirect('Orders')
        return redirect('Orders')


class OrderView(View):
    def get(self, request):
        page = request.GET.get('page')
        user = request.user
        try:
            orders = Order.objects.filter(user=user).order_by('-date').exclude(order_status="PENDING")
            if page is None and page == "":
                page = 1
            paginator = Paginator(orders, 5)
            page_object = paginator.get_page(page)
        except:
            page_object = None


        context = {
            "page_object": page_object,
        }

        return render(request, 'store/order.html', context=context)



