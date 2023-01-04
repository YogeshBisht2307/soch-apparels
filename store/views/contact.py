import os
from math import floor
from store.models import Contact
from django.http import HttpResponse
from typing import Optional, Tuple, Dict
from django.views.generic.base import View
from django.core.mail import send_mass_mail
from django.shortcuts import render, redirect
from SochApparels.settings import EMAIL_HOST_USER
from django.core.handlers.wsgi import WSGIRequest


class ContactView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        return render(request, 'store/contact.html')

    def post(self, request: WSGIRequest) -> HttpResponse:
        name: str = request.POST.get('name')
        email: str = request.POST.get('email')
        subject: str = request.POST.get('subject')
        message: str = request.POST.get('message')

        error_message: Optional[str] = None
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

        if not error_message:
            contact: Contact = Contact()
            contact.name = name
            contact.email = email
            contact.subject = subject
            contact.message = message
            contact.save()

            user_message: Tuple = ('Product Issue Submitted',
                            f"We have recieved your query regarding :- {contact.subject}, we will try to resolve is soon",
                            os.environ['SENDER_EMAIL'], [contact.email])

            host_message: Tuple = (contact.subject,
                            f"You have recieved a email regarding product or website issue from {contact.email} . The message is as follow :- {contact.message}",
                            os.environ['SENDER_EMAIL'], [EMAIL_HOST_USER])

            send_mass_mail((user_message, host_message), fail_silently=False)
            return render(request, 'store/contact.html', {"success": "Your request has recieved , we will response to it soon ! "})
        else:
            context: Dict = {
                "error_message": error_message,
                "name": name,
                "email": email,
                "message": message,
                "subject": subject
            }
            return render(request, 'store/contact.html', context=context)

