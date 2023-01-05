from store.views import *
from typing import List
from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

admin.site.site_title = "Welcome to SochApparels Admin DashBoard"
admin.site.index_title = "Welcome to SochApparels Portal"

urlpatterns: List = [
    path("", IndexView.as_view() , name="Home"),
    path("about/", AboutView.as_view(), name="About"),
    path("store/", StoreView.as_view(), name = "Store"),
    path("login/", LoginView.as_view(), name="Login"),
    path("registration/", RegistrationView.as_view(), name="Registration"),
    path("logout/", LogoutView.as_view(), name="Logout"),
    path("contact/", ContactView.as_view(), name= "Contact"),
    path("cart/",CartView.as_view(), name="Cart"),
    path("addtocart/<str:cloth_slug>/<str:size>", AddCartView.as_view(), name = "AddtoCart"),
    path("removecart/<str:cloth_slug>/<str:size>", RemoveCartView.as_view(), name="RemoveCart"),
    path("product_detail/<str:cloth_slug>", ProductDetailView.as_view(), name="ProductDetail"),
    path("checkout/", login_required(CheckoutView.as_view(), login_url="/login/"), name="Checkout"),
    path("validate_payment/", validate_payment, name="ValidatePayment"),
    path("payment_failed/", login_required(PaymentFailed.as_view(), login_url="/login/"), name="PaymentFailed"),
    path('orders/', login_required(OrderView.as_view(),login_url="/login/") , name="Orders"),
    path('cancel_order/', CancelOrderView.as_view(), name="CancelOrder"),
    path('comments/',login_required(CommentView.as_view(), login_url="/login/"), name="Comment"),
    path('buy/', BuyView.as_view(),name="Buy"),

    path('password_reset/',
        auth_views.PasswordResetView.as_view(template_name="store/registration/password_reset_form.html"),
        name="reset_password"
    ),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name="store/registration/password_reset_done.html"),
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="store/registration/password_reset_confirm.html"),
        name='password_reset_confirm'
    ),
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name="store/registration/password_reset_complete.html"),
        name='password_reset_complete'
    )
]