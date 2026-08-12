from django.urls import path
from .views import (
                    LSASearchAPIView,
                     BookingCreateAPIView,
                     mock_payment_api,
                    payment_webhook,
                     )

urlpatterns = [
    path("v1/lsas/search/", LSASearchAPIView.as_view(), name="lsa-search"),
    path("v1/bookings/", BookingCreateAPIView.as_view(), name="booking-create"),
    path("v1/mock-payment/", mock_payment_api, name="mock-payment"),
    path("v1/payments/webhook/", payment_webhook, name="payment-webhook"),
]
