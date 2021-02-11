from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Cloth, Size_Variant, Cart, Order, Order_Item, Payment, Occasion, Category, Sub_Category, Color, \
    Brand, Comment, Contact
from math import floor
from django.contrib.auth.decorators import login_required
from store.forms.authforms import CustomerCreationForm, \
    CustomerAuthenticationForm  # imporing the class from froms folder
from django.contrib.auth import authenticate, login as loginUser
from django.views.generic.base import View
from django.core.mail import send_mass_mail
from SochApparels.settings import EMAIL_HOST_USER


class ContactView(View):
    def get(self, request):
        return render(request, 'store/contact.html')

    def post(self, request):

        query = request.POST
        name = query.get('name')
        email = query.get('email')
        subject = query.get('subject')
        message = query.get('message')

        error_message = None
        if name == "":
            error_message = "Name is required"
        elif len(name) < 4:
            error_messge = "Enter a correct name"
        elif email == "":
            error_message = "Email is required"
        elif len(email) < 10:
            error_message = "Enter a correct email"
        elif subject == "":
            error_message = "Subject is required"
        elif len(subject) < 10:
            error_message = "Enter a readable Subject"
        elif message == "" and len(message) < 20:
            error_message = "Explain your Subject properly"

        # saving the contact information
        if error_message is None:
            contact = Contact()
            contact.name = name
            contact.email = email
            contact.subject = subject
            contact.message = message
            contact.save()

            user_message = ('Product Issue Submitted',
                            f"We have recieved your query regarding :- {contact.subject}, we will try to resolve is soon",
                            'Yogeshbisht.2307@gmail.com', [contact.email])

            host_message = (contact.subject,
                            f"You have recieved a email regarding product or website issue from {contact.email} . The message is as follow :- {contact.message}",
                            'Yogeshbisht.2307@gmail.com', [EMAIL_HOST_USER])

            send_mass_mail(
                (user_message,
                 host_message),
                fail_silently=False
            )
            return render(request, 'store/contact.html',
                          {"success": "Your request has recieved , we will response to it soon ! "})
        else:
            context = {
                "error_message": error_message,
                "name": name,
                "email": email,
                "message": message,
                "subject": subject
            }
            return render(request, 'store/contact.html', context=context)

