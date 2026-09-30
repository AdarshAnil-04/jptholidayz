import datetime
from django.test import TestCase
from apps.accounts.models import User
from apps.destinations.models import Destination
from apps.packages.models import TravelPackage
from .models import Booking, BookingStatusHistory

class BookingWorkflowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='customer1', password='pass')
        self.staff = User.objects.create_user(username='staff1', password='pass', role=User.Role.BOOKING_STAFF)
        self.destination = Destination.objects.create(name='Paris', country='France', description='City of lights')
        self.package = TravelPackage.objects.create(
            destination=self.destination,
            title='Paris Romance Holiday',
            overview='Eiffel Tower views.',
            duration_days=4,
            price_per_person=1500.00,
            status=TravelPackage.Status.PUBLISHED
        )

    def test_booking_request_creation_and_ref_generation(self):
        booking = Booking.objects.create(
            customer=self.user,
            guest_name='Alex Morgan',
            guest_email='alex@example.com',
            guest_phone='+1 555-0192',
            package=self.package,
            travel_date=datetime.date.today() + datetime.timedelta(days=15),
            adults_count=2,
            children_count=0
        )
        self.assertTrue(booking.reference_code.startswith('JPT-'))
        self.assertEqual(booking.status, Booking.Status.PENDING)
        self.assertEqual(booking.total_quoted_price, 3000.00) # 2 adults * 1500

    def test_booking_status_transition_and_history(self):
        booking = Booking.objects.create(
            guest_name='John Doe',
            guest_email='john@example.com',
            guest_phone='12345',
            package=self.package,
            travel_date=datetime.date.today() + datetime.timedelta(days=20),
            adults_count=1
        )
        booking.transition_to(Booking.Status.UNDER_REVIEW, user=self.staff, note='Reviewing dates.')
        self.assertEqual(booking.status, Booking.Status.UNDER_REVIEW)
        self.assertEqual(booking.status_history.count(), 1)
        self.assertEqual(booking.status_history.first().to_status, Booking.Status.UNDER_REVIEW)
