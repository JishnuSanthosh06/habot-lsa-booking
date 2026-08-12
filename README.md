# LSA Booking API

A Django REST Framework based API for searching Language Support Assistants (LSAs), creating booking requests, preventing overlapping bookings, and handling mock payment processing and payment webhooks.

## Features

- LSA profile management
- Skill-based LSA search
- Parent management
- Booking creation
- Booking time validation
- Double-booking prevention
- Booking status management
- Mock payment processing
- Payment success/failure webhook
- Automated API tests
- GitHub Actions CI

## Technology Stack

- Python
- Django
- Django REST Framework
- SQLite
- Git & GitHub
- GitHub Actions

## Project Structure

```text
habot-lsa-booking/
│
├── bookings/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md