from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import User
from .models import Wish


from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def index(req):

    if "user_id" not in req.session:
        return redirect("users:new")

    else:
        context = {
            "user": User.objects.get(id=req.session["user_id"]),
            "wishes": Wish.objects.order_by("-created_at"),
        }
    return render(req, "wishes/wishes.html", context)


def add(req):
    if "user_id" not in req.session:
        return redirect("users:new")
    else:
        context = {"user": User.objects.get(id=req.session["user_id"])}
        return render(req, "wishes/addwish.html", context)


def create(req):
    errors = Wish.objects.validate(req.POST)
    if errors:
        for error in errors:
            messages.error(req, error)
        return redirect("wishes:add")
    else:
        Wish.objects.create_wish(req.POST, req.session["user_id"])
        print(req.POST)
    return redirect("wishes:index")


def edit(req, wish_id):
    if "user_id" not in req.session:
        return redirect("users:new")

    try:
        context = {
            "user": User.objects.get(id=req.session["user_id"]),
            "wish": Wish.objects.get(id=wish_id),
        }
        print(req.POST)
    except ObjectDoesNotExist:
        return redirect("wishes:index")

    return render(req, "wishes/edit.html", context)


def update(req, wish_id):
    errors = Wish.objects.validate(req.POST)
    if errors:
        for error in errors:
            messages.error(req, error)
        return redirect("wishes:edit", wish_id=wish_id)
    Wish.objects.update(req.POST, wish_id)
    return redirect("wishes:index")


def delete(req, wish_id):
    try:
        wish = Wish.objects.get(id=wish_id)
        wish.delete()

    except ObjectDoesNotExist:
        print("TRIED TO DELETE Wish #{}, DOES NOT EXIST".format(wish_id))

    return redirect("wishes:index")


def like(req, wish_id):
    Wish.objects.add_like(req.session["user_id"], wish_id)
    return redirect("wishes:index")


def unlike(req, wish_id):
    Wish.objects.remove_like(req.session["user_id"], wish_id)
    return redirect("wishes:index")


def viewstats(req):
    if "user_id" not in req.session:
        return redirect("users:new")

    else:
        user = User.objects.get(id=req.session["user_id"])
    context = {
        "user": user,
        "grantedwishes": Wish.objects.annotate(x=Count("granted")).filter(granted=True),
        "usergranted": Wish.objects.annotate(x=Count("granted")).filter(
            granted=True, creator=user
        ),
        "userpending": Wish.objects.annotate(x=Count("granted")).filter(
            granted=False, creator=user
        ),
    }
    return render(req, "wishes/viewstats.html", context)


def grant(req, wish_id):
    if "user_id" not in req.session:
        return redirect("users:new")

    else:
        wish = Wish.objects.get(id=wish_id)
        wish.granted = True
        wish.save()
        print(req.POST)
    return redirect("wishes:index")

