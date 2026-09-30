from django.test import TestCase
from apps.destinations.models import Destination
from .models import TravelPackage, ItineraryDay

class PackageCatalogTests(TestCase):
    def setUp(self):
        self.destination = Destination.objects.create(
            name='Maldives',
            country='Maldives',
            description='Tropical island paradise'
        )

    def test_create_package_and_slug_auto_generation(self):
        package = TravelPackage.objects.create(
            destination=self.destination,
            title='Maldives Overwater Bungalow Escape',
            overview='Exclusive water villa holiday.',
            duration_days=6,
            duration_nights=5,
            price_per_person=1999.00,
            status=TravelPackage.Status.PUBLISHED
        )
        self.assertEqual(package.slug, 'maldives-overwater-bungalow-escape')
        self.assertEqual(package.destination.package_count, 1)

    def test_itinerary_days_relationship(self):
        package = TravelPackage.objects.create(
            destination=self.destination,
            title='Resort Stay',
            overview='Short resort holiday.',
            price_per_person=800.00
        )
        day1 = ItineraryDay.objects.create(
            package=package,
            day_number=1,
            title='Speedboat Transfer',
            description='Arrival at Male international airport and speedboat transfer.'
        )
        self.assertEqual(package.itinerary_days.count(), 1)
        self.assertEqual(day1.package, package)
