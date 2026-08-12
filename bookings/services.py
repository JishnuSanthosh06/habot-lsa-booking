import logging
import requests


logger = logging.getLogger(__name__)


class PaymentService:

    MOCK_PAYMENT_URL = "http://127.0.0.1:8000/api/v1/mock-payment/"

    @staticmethod
    def process_payment(booking_id, amount):
        payload = {
            "booking_id": booking_id,
            "amount": amount,
        }

        try:
            response = requests.post(
                PaymentService.MOCK_PAYMENT_URL,
                json=payload,
                timeout=5,
            )

            response.raise_for_status()

            logger.info(
                "Payment processed successfully for booking %s",
                booking_id,
            )

            return {
                "success": True,
                "message": "Payment processed successfully.",
            }

        except requests.exceptions.Timeout:
            logger.error(
                "Payment request timed out for booking %s",
                booking_id,
            )

            return {
                "success": False,
                "message": "Payment service timed out.",
            }

        except requests.exceptions.RequestException as error:
            logger.error(
                "Payment request failed for booking %s: %s",
                booking_id,
                error,
            )

            return {
                "success": False,
                "message": "Payment service unavailable.",
            }