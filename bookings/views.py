from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import LSAProfile, BookingRequest
from .serializers import (
    LSASearchSerializer,
    BookingRequestSerializer,
)


class LSASearchAPIView(APIView):

    def get(self, request):
        skill_name = request.query_params.get("skill")

        queryset = (
            LSAProfile.objects
            .filter(is_active=True)
            .prefetch_related("skills")
        )

        if skill_name:
            queryset = queryset.filter(
                skills__name__iexact=skill_name
            )

        queryset = queryset.distinct()

        serializer = LSASearchSerializer(
            queryset,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class BookingCreateAPIView(APIView):

    def post(self, request):
        serializer = BookingRequestSerializer(
            data=request.data
        )

        if serializer.is_valid():
            booking = serializer.save()

            return Response(
                BookingRequestSerializer(booking).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def mock_payment_api(request):

    amount = request.data.get("amount")

    if not amount:
        return Response(
            {
                "success": False,
                "message": "Amount is required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {
            "success": True,
            "transaction_id": "MOCK_TXN_12345",
            "message": "Payment Successful."
        },
        status=status.HTTP_200_OK
    )


@api_view(["POST"])
def payment_webhook(request):

    booking_id = request.data.get("booking_id")
    payment_status = request.data.get("payment_status")

    if not booking_id or not payment_status:
        return Response(
            {
                "success": False,
                "message": "booking_id and payment_status are required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        booking = BookingRequest.objects.get(
            id=booking_id
        )

    except BookingRequest.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "Booking not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    if payment_status == "SUCCESS":

        booking.payment_status = (
            BookingRequest.PaymentStatus.SUCCESS
        )

        booking.status = (
            BookingRequest.Status.CONFIRMED
        )

        booking.save(
            update_fields=[
                "payment_status",
                "status",
            ]
        )

        return Response(
            {
                "success": True,
                "message": "Payment successful. Booking confirmed.",
                "booking_id": booking.id,
                "payment_status": booking.payment_status,
                "booking_status": booking.status,
            },
            status=status.HTTP_200_OK
        )

    elif payment_status == "FAILED":

        booking.payment_status = (
            BookingRequest.PaymentStatus.FAILED
        )

        booking.status = (
            BookingRequest.Status.PAYMENT_FAILED
        )

        booking.save(
            update_fields=[
                "payment_status",
                "status",
            ]
        )

        return Response(
            {
                "success": True,
                "message": "Payment failed. Booking updated.",
                "booking_id": booking.id,
                "payment_status": booking.payment_status,
                "booking_status": booking.status,
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            "success": False,
            "message": "Invalid payment status."
        },
        status=status.HTTP_400_BAD_REQUEST
    )