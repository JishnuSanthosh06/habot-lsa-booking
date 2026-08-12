from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from .models import Parent, Skill, LSAProfile, BookingRequest

class BookingAPITestCase(APITestCase):
    def setUp(self):
        self.parent = Parent.objects.create(
            name="Rahul",
            email="rahul@test.com",
            phone="9876543210"
        )
        self.skill = Skill.objects.create(
            name = "English"
        )

        self.lsa = LSAProfile.objects.create(
            name= "Anu",
            email="anu@test.com"
        )

        self.lsa.skills.add(self.skill)

        self.start_time = timezone.now() + timedelta(days=1)
        self.end_time = self.start_time + timedelta(hours=1)

    def test_lsa_search(self):
        response = self.client.get(
            "/api/v1/lsas/search/?skill=English"
        ) 

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_booking(self):
        data = {
            "parent":self.parent.id,
            "lsa":self.lsa.id,
            "start_time":self.start_time.isoformat(),
            "end_time":self.end_time.isoformat(),
        }

        response = self.client.post(
            "/api/v1/bookings/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            response.data["status"],
            "PENDING"
        )

        self.assertEqual(
            response.data["payment_status"],
            "PENDING"
        )

    def test_invalid_time_range(self):
        data = {
            "parent":self.parent.id,
            "lsa":self.lsa.id,
            "start_time":self.end_time.isoformat(),
            "end_time":self.start_time.isoformat(),
        }
        response = self.client.post(
            "/api/v1/bookings/",
            data,
            format = "json"
        )

        self.assertEqual(response.status_code, 400)

    def test_doubleBooking_is_rejected(self):
        BookingRequest.objects.create(
            parent=self.parent,
            lsa=self.lsa,
            start_time=self.start_time,
            end_time=self.end_time
        )

        overalpping_start = self.start_time + timedelta(minutes=30)
        overalpping_end = overalpping_start +timedelta(hours=1)

        data ={
            "parent":self.parent.id,
            "lsa":self.lsa.id,
            "start_time":overalpping_start.isoformat(),
            "end_time":overalpping_end.isoformat(),
            }
        response = self.client.post(
            "/api/v1/bookings/",
            data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_payment_bebhook_success(self):
        booking = BookingRequest.objects.create(
            parent = self.parent,
            lsa = self.lsa,
            start_time = self.start_time,
            end_time= self.end_time
        )

        data = {
            "booking_id":booking.id,
            "payment_status":"SUCCESS"
        }

        response = self.client.post(
            "/api/v1/payments/webhook/",
            data,
            format= "json"
        )

        self.assertEqual(response.status_code, 200)

        booking.refresh_from_db()

        self.assertEqual(
            booking.payment_status,
            "SUCCESS"
        )

        self.assertEqual(
            booking.status,
            "CONFIRMED"
        )

    def test_payemnt_webhook_failures(self):
        booking = BookingRequest.objects.create(
            parent=self.parent,
            lsa=self.lsa,
            start_time=self.start_time,
            end_time=self.end_time
        )

        data = {
            "booking_id":booking.id,
            "payment_status":"FAILED"
        }

        response = self.client.post(
            "/api/v1/payments/webhook/",
            data,
            format = "json"
        )

        self.assertEqual(response.status_code, 200)

        booking.refresh_from_db()


        self.assertEqual(
            booking.payment_status,
            "FAILED"
        )

        self.assertEqual(
            booking.status,
            "PAYMENT_FAILED"
        )
