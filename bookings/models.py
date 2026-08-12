from django.db import models
from django.core.exceptions import ValidationError


class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class LSAProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    skills = models.ManyToManyField(
        Skill,
        related_name="lsas"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BookingRequest(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAYMENT_PENDING = "PAYMENT_PENDING", "Payment Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        PAYMENT_FAILED = "PAYMENT_FAILED", "Payment Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    parent = models.ForeignKey(
        Parent,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    lsa = models.ForeignKey(
        LSAProfile,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(
                "End time must be after start time."
            )

    def __str__(self):
        return f"{self.parent.name} - {self.lsa.name}"