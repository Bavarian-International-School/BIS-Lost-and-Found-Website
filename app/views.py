import os
from datetime import datetime

import cv2
import numpy as np
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required  # for function based view
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator  # for class based view
from django.views import View
from dotenv import load_dotenv
from django.conf import settings

from hawkeye.hawkeye import Hawkeye
from postmaster.postmaster import PostMaster

from .forms import (
    CustomerProfileForm,
    CustomerRegistrationForm,
    EmailForm,
    ImageUploadForm,
)
from .models import Customer, LostItem

load_dotenv()


def base(request):

    context = {
        "categories": [
            {
                "name": name,
                "items": LostItem.objects.filter(status="Lost", category=code),
            }
            for code, name in LostItem.CATEGORY_CHOICES
        ],
    }

    return render(request, "base.html", context)


def home(request):
    image_extensions = [
        ".png",
        ".jpg",
        ".jpeg",
        ".jfif",
        ".pjpeg",
        ".pjp",
        ".svg",
        ".webp",
        ".aviff",
    ]
    images = [
        os.path.join("banner", image)
        for image in os.listdir(f"{settings.BASE_DIR}/app/static/banner/")
        if any(image.endswith(ext) for ext in image_extensions)
    ]
    context = {
        "categories": [
            {
                "name": name,
                "items": LostItem.objects.filter(status="Lost", category=code),
            }
            for code, name in LostItem.CATEGORY_CHOICES
        ],
        "images": images,
    }

    return render(request, "home.html", context)


class LostItemDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        item = LostItem.objects.get(pk=pk)
        return render(
            request,
            "itemdetail.html",
            {"product": item},
        )


def lost_item_detail_view(request, pk):
    item = LostItem.objects.get(pk=pk)
    return render(request, "itemdetail.html", {"product": item})


@method_decorator(login_required, name="dispatch")
class ClaimItemView(View):
    def get(self, request: HttpRequest, *arg, **kwarg):
        return redirect("home")

    def post(self, request: HttpRequest, item_id: int, *arg, **kwarg) -> HttpResponse:
        item = LostItem.objects.get(pk=item_id)
        item.status = "ClaimPlaced"
        item.claimed_by = self.request.user  # type: ignore
        item.save()
        return render(
            request,
            "claim.html",
            {"product": item},
        )


@staff_member_required
def claims(request):
    items = LostItem.objects.filter(status="ClaimPlaced").order_by("category")
    return render(request, "claims.html", {"items": items})


def login(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")


def logout_sucess(request: HttpRequest) -> HttpResponse:  # type: ignore
    if request.method == "POST" or request.method == "GET":
        logout(request)
        return render(request, "logout.html")


class CustomerRegistrationView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = CustomerRegistrationForm()
        return render(request, "registration.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations!! Registered Successfully")
            form.save()
        return render(request, "registration.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = CustomerProfileForm()
        return render(request, "profile.html", {"form": form, "active": "btn-primary"})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data["name"]
            reg = Customer(
                user=usr,
                name=name,
            )
            reg.save()
            messages.success(request, "Congratulations!! Profile Updated Successfully")
        return render(request, "profile.html", {"form": form, "active": "btn-primary"})


def search_results(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        search = request.POST["search"]
        results = LostItem.objects.filter(description__contains=search)
        return render(
            request, "search_results.html", {"search": search, "results": results}
        )

    else:
        return render(
            request,
            "search_results.html",
            {"search": search, "results": "No Results found"},  # type: ignore
        )


@login_required
def newsletter(request: HttpRequest) -> HttpResponse:
    user = request.user
    if user.is_superuser:  # type: ignore
        if request.method == "POST":
            form = EmailForm(request.POST)
            if not all(
                os.environ.get(var)
                for var in ["MAILJET_API_KEY", "MAILJET_API_SECRET", "MAILJET_EMAIL"]
            ):
                return HttpResponse(
                    "The Mailjet API key and secret have not been set. Please follow the install instructions on how to do so"
                )

            if form.is_valid():
                message = form.cleaned_data["message"]
                newsletter_users = Customer.objects.filter(newsletter_signup=True)
                user_mails = [user.mail for user in newsletter_users]
                if user_mails is None:
                    return HttpResponse("No users have signed up for the newsletter")
                postmaster = PostMaster(
                    os.environ.get("MAILJET_API_KEY"),  # type: ignore
                    os.environ.get("MAILJET_API_SECRET"),  # type: ignore
                )
                postmaster.send_email(
                    os.environ.get("MAILJET_EMAIL"),  # type: ignore
                    user_mails,
                    "BIS Lost and Found Newsletter",
                    message,
                )
                return HttpResponse(
                    "Emails sent. to " + str(user_mails) + " with message: " + message
                )

        else:
            form = EmailForm()
        return render(request, "newsletter.html", {"form": form})
    else:
        customer, created = Customer.objects.get_or_create(
            user=user, defaults={"name": user.username, "mail": user.email}  # type: ignore
        )
        if customer.newsletter_signup == True:
            customer.newsletter_signup = False
            customer.mail = user.email  # type: ignore
            customer.save()
            return HttpResponse("Unregistered form the newsletter.")
        else:
            customer.newsletter_signup = True
            customer.save()
            return HttpResponse("Registered for the newsletter.")


@staff_member_required
def hawkeye(request: HttpRequest) -> HttpResponse:
    form = ImageUploadForm(request.POST, request.FILES)
    hawkeye = Hawkeye()
    if request.method == "POST":
        images = request.FILES.getlist("image")
        for image in images:
            img = cv2.imdecode(
                np.frombuffer(image.read(), np.uint8), cv2.IMREAD_UNCHANGED
            )
            img = hawkeye.img_array_to_processed_array(img)  # Processed array
            prediction = hawkeye.predict(img)
            name = hawkeye.get_class_name(prediction)
            description = f"Item {name} has been automatically classifed by Hawkeye™ Image Classifier. There may be errors in the classification algorithm"
            category = hawkeye.get_model_name(prediction)[0]  # type: ignore
            image_model = LostItem(
                name=name,
                category=category,
                description=description,
                image=image,
                date_found=datetime.now(),
                status="Lost",
            )
            image_model.save()

        return redirect("home")
    context = {"form": form}
    return render(request, "hawkeye.html", context)
