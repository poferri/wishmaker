from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from apps.wishes.models import Wish


# Create your views here.


def new(req):
    return render(req, "users/new.html")


def create(req):
    errors = User.objects.validate(req.POST)
    if errors:
        for error in errors:
            messages.error(req, error)
            return redirect("users:new")
    else:
        user = User.objects.create_user(req.POST)
        req.session["user_id"] = user.id
    return redirect("wishes:index")


def login(req):
    valid, result = User.objects.login(req.POST)
    if not valid:
        messages.error(req, result)
        return redirect("users:new")
    else:
        req.session["user_id"] = result.id
    return redirect("wishes:index")


def logout(req):
    req.session.clear()

    return redirect("users:new")
