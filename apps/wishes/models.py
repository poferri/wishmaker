from django.db import models
from ..users.models import User
from datetime import datetime


# Create your models here.
class WishManager(models.Manager):
    def validate(self, form_data):
        errors = []

        if len(form_data["item"]) < 3:
            errors.append("Name must be at least 2 characters long.")
        if len(form_data["description"]) < 3:
            errors.append("Must include a description")
        if len(form_data["description"]) > 255:
            errors.append("Description must be less than 255 characters")

        return errors

    def create_wish(self, form_data, user_id):
        user = User.objects.get(id=user_id)
        Wish.objects.create(
            item=form_data["item"],
            description=form_data["description"],
            wisher=form_data["wisher"],
            creator=user,
        )

    def update(self, form_data, wish_id):
        wish = self.get(id=wish_id)
        wish.item = form_data["item"]
        wish.description = form_data["description"]
        wish.wisher = form_data["wisher"]
        wish.save()

    def add_like(self, user_id, wish_id):
        user = User.objects.get(id=user_id)
        wish = Wish.objects.get(id=wish_id)
        user.liked.add(wish)
        user.save()

    def remove_like(self, user_id, wish_id):
        user = User.objects.get(id=user_id)
        wish = Wish.objects.get(id=wish_id)
        user.liked.remove(wish)


class Wish(models.Model):
    item = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    granted = models.BooleanField(default=False)
    wisher = models.CharField(max_length=255)
    date_granted = models.DateField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="liked")
    creator = models.ForeignKey(User, related_name="wishes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()

    def __repr__(self):
        return "<User: %s>" % self.email

    def __str__(self):
        return "<User: %s>" % self.email

