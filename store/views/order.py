from math import floor
from typing import Dict
from django.contrib import messages
from django.views.generic.base import View
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from django.core.handlers.wsgi import WSGIRequest

from store.models import *
from django.core.mail import send_mail
from SochApparels.settings import EMAIL_HOST_USER



class CancelOrderView(View):
    def get(self, request: WSGIRequest) -> response.HttpResponseRedirect:
        user = request.user
        order_id: str = request.GET.get('oddl')
        order: Order = Order.objects.get(id=order_id)
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
    def get(self, request) -> HttpResponse:
        page: int = request.GET.get('page')
        user = request.user
        orders: Order = Order.objects.filter(user=user).order_by('-date').exclude(order_status="PENDING")
        page = 1 if not page else page
        paginator: Paginator = Paginator(orders, 5)
        page_object = paginator.get_page(page)
        context: Dict = {
            "page_object": page_object,
        }
        return render(request, 'store/order.html', context=context)
