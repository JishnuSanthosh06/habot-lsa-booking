from rest_framework import serializers
from  .models import LSAProfile, BookingRequest

class LSASearchSerializer(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = LSAProfile
        fields = ["id", "name", "email", "skills", "is_active", ]

class BookingRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingRequest
        fields = [
            "id",
            "parent",
            "lsa",
            "start_time",
            "end_time",
            "status",
            "payment_status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "payment_status",
            "created_at",
        ]

    def validate(self, data):
        start_time = data["start_time"]
        end_time = data["end_time"]
        lsa = data["lsa"]

        if start_time >= end_time:
            raise serializers.ValidationError(
                "End time must be after start time."
            )

        overlapping_booking = BookingRequest.objects.filter(
            lsa=lsa,
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).exclude(
            status=BookingRequest.Status.CANCELLED
        ).exists()

        if overlapping_booking:
            raise serializers.ValidationError(
                "This LSA is already booked during the requested time."
            )

        return data