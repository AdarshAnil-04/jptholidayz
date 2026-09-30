import datetime
from django.test import TestCase
from apps.destinations.models import Destination
from apps.packages.models import TravelPackage, ItineraryDay
from apps.bookings.models import Booking
from .pdf_generator import generate_booking_itinerary_pdf

class PDFItineraryGeneratorTests(TestCase):
    def test_pdf_generation_stream(self):
        destination = Destination.objects.create(name='Rome', country='Italy', description='Eternal city')
        package = TravelPackage.objects.create(
            destination=destination,
            title='Rome Historic Tour',
            overview='Colosseum & Vatican.',
            duration_days=3,
            price_per_person=900.00
        )
        ItineraryDay.objects.create(
            package=package,
            day_number=1,
            title='Arrival & Colosseum',
            description='Tour Colosseum and Roman Forum.'
        )
        booking = Booking.objects.create(
            guest_name='Test Traveler',
            guest_email='traveler@example.com',
            guest_phone='1234567890',
            package=package,
            travel_date=datetime.date.today() + datetime.timedelta(days=10),
            adults_count=2,
            status=Booking.Status.CONFIRMED
        )

        pdf_buffer = generate_booking_itinerary_pdf(booking)
        pdf_bytes = pdf_buffer.getvalue()
        self.assertTrue(pdf_bytes.startswith(b'%PDF'))
        self.assertGreater(len(pdf_bytes), 1000)
