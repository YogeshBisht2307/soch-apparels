from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Cloth, Size_Variant, Cart, Order, Order_Item, Payment, Occasion, Category, Sub_Category, Color, \
    Brand, Comment
from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Cloth, Size_Variant, Cart, Order, Order_Item, Payment, Occasion, Category, Sub_Category, Color, \
    Brand, Comment
from math import floor
from django.contrib.auth.decorators import login_required
from store.forms.authforms import CustomerCreationForm, \
    CustomerAuthenticationForm  # imporing the class from froms folder
from django.contrib.auth import authenticate, login as loginUser
from store.forms.checkout_form import CheckoutForm
import razorpay
from SochApparels.settings import KEY_ID, KEY_SECRET
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from SochApparels.settings import EMAIL_HOST_USER


@csrf_exempt
def validate_payment(request):
    user = None
    # getting login user
    if request.user.is_authenticated:
        user = request.user

    # fetching payment detail
    order_detail = request.POST
    order_id = order_detail.get('razorpay_order_id')
    payment_id = order_detail.get('razorpay_payment_id')
    signature = order_detail.get('razorpay_signature')

    # verifying payment signature
    client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
    payment_info = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    payment_status = client.utility.verify_payment_signature(payment_info)

    if payment_status is None:
        try:
            # updating payment if staus is not failed
            payment = Payment.objects.get(payment_request_id=order_id)
            payment.payment_id = payment_id
            payment.payment_status = "SUCCESS"
            payment.save()

            # updating order
            order = payment.order
            order.order_status = "PLACED"
            order.save()
            # deleting cart after order placed
            buy = []
            request.session['buy']= buy
            cart = []
            request.session['cart'] = cart

            # deleting cart from session
            Cart.objects.filter(user=user).delete()

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
                    'Yogeshbisht.2307@gmail.com',
                    [user.email],
                    fail_silently=False,
                    html_message=html_message,
                )
                # mail to user
                send_mail(
                    'Product Purchased',
                    f"You have recieved a {order.total}Rupee Payment for order id = {order.id}, check it out and procced for delivery",
                    'Yogeshbisht.2307@gmail.com',
                    [EMAIL_HOST_USER],
                    fail_silently=False,
                )
            except:
                return redirect('Orders')
            return redirect("Orders")
        except:
            return render(request, 'store/payment_failed.html')
    else:
        # //error page
        return render(request, 'store/payment_failed.html')

