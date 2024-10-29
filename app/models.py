from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mail = models.EmailField(unique=True)
    newsletter_signup = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class LostItem(models.Model):
    CATEGORY_CHOICES = (
        ("EL", "Electronics"),
        ("TW", "Topwear"),
        ("BW", "Bottomwear"),
        ("JK", "Jackets"),
        ("FW", "Footwear"),
        ("ST", "Stationaries"),
        ("BG", "Bags"),
        ("AC", "Accessories"),
        ("LB", "Lunchboxes"),
        ("WB", "Waterbottles"),
        ("VB", "Valuables"),
        ("OT", "Others"),
    )

    STATUS_CHOICES = (
        ("Lost", "Lost"),
        ("Claimed", "Claimed"),
        ("Unclaimed", "Unclaimed"),
        ("ClaimPlaced", "ClaimPlaced"),
        ("Storage", "Storage"),
    )

    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField()
    date_found = models.DateField(auto_now_add=True)  # Automatically set today's date
    location_found = models.CharField(max_length=200)
    claimed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="claimed_items",  # Fix Reverse accessor clash in Django
        null=True,
        blank=True,
    )
    found_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="found_items",  # Fix Reverse accessor clash in Django
        null=True,
        blank=True,
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="Lost")

    def __str__(self):
        return f"{self.name} ({self.category})"

    def delete(
        self, *args, **kwargs
    ):  # Overwrite the built in delete command to delete the image when an item is deleted.
        self.image.delete(save=False)
        super().delete(*args, **kwargs)
