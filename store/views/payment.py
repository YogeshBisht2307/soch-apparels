import razorpay
from math import floor
from django.template import loader
from django.core.mail import send_mail
from typing import Dict, List, Optional
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt

from store.models import Cart, Order, Payment
from SochApparels.settings import KEY_ID, KEY_SECRET
from SochApparels.settings import EMAIL_HOST_USER


class PaymentFailed(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        return render(request, 'store/payment_failed.html')


@csrf_exempt
def validate_payment(request: WSGIRequest) -> response.HttpResponseRedirect:
    user = request.user if request.user.is_authenticated else None
    order_id: str = request.POST.get('razorpay_order_id')
    payment_id: str = request.POST.get('razorpay_payment_id')
    signature: str = request.POST.get('razorpay_signature')

    client: razorpay.Client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
    payment_info = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    try:
        payment_status: bool = client.utility.verify_payment_signature(payment_info)
        if not payment_status:
            request.session['buy']= []
            return redirect("PaymentFailed")
    except Exception:
        request.session['buy']= []
        return redirect("PaymentFailed")

    payment: Payment = Payment.objects.get(payment_request_id=order_id)
    payment.payment_id = payment_id
    payment.payment_status = "SUCCESS"
    payment.save()

    order: Order = payment.order
    order.order_status = "PLACED"
    order.save()

    Cart.objects.filter(user=user).delete()
    request.session['cart'] = []
    request.session['buy']= []
    return redirect("Orders")
