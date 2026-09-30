from django.core.management.base import BaseCommand
from apps.accounts.models import User, CustomerProfile, StaffProfile
from apps.destinations.models import Destination
from apps.packages.models import TravelPackage, ItineraryDay
from apps.gallery.models import GalleryCategory, GalleryImage
from apps.bookings.models import Booking
from apps.core.models import SiteSettings
import datetime

class Command(BaseCommand):
    help = 'Seeds initial sample data for JPT Holidays platform'

    def handle(self, *args, **options):
        self.stdout.write("Seeding data for JPT Holidays...")

        # 1. Site Settings
        settings_obj = SiteSettings.load()
        settings_obj.site_name = "JPT Holidays"
        settings_obj.tagline = "Bespoke Travel, Curated Holiday Packages & Luxury Escapes"
        settings_obj.contact_email = "desk@jptholidays.com"
        settings_obj.contact_phone = "+1 (800) 578-4654 [Agency Phone Placeholder]"
        settings_obj.whatsapp_number = "+1 (800) 578-4655 [WhatsApp Placeholder]"
        settings_obj.office_address = "450 Tourism Boulevard, Suite 800, New York, NY 10001 [Placeholder Address]"
        settings_obj.save()

        # 2. Users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@jptholidays.com',
                'first_name': 'Super',
                'last_name': 'Admin',
                'role': User.Role.SUPER_ADMIN,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created Super Admin (user: admin, pass: admin123)"))

        staff_user, created = User.objects.get_or_create(
            username='staff',
            defaults={
                'email': 'staff@jptholidays.com',
                'first_name': 'Sarah',
                'last_name': 'Jenkins',
                'role': User.Role.BOOKING_STAFF,
                'is_staff': True
            }
        )
        if created:
            staff_user.set_password('staff123')
            staff_user.save()
            StaffProfile.objects.get_or_create(user=staff_user, employee_id='EMP-001', job_title='Lead Travel Consultant')
            self.stdout.write(self.style.SUCCESS("Created Booking Staff (user: staff, pass: staff123)"))

        customer_user, created = User.objects.get_or_create(
            username='customer',
            defaults={
                'email': 'customer@example.com',
                'first_name': 'Alex',
                'last_name': 'Morgan',
                'role': User.Role.CUSTOMER
            }
        )
        if created:
            customer_user.set_password('customer123')
            customer_user.save()
            CustomerProfile.objects.get_or_create(user=customer_user, address='123 Traveler St')
            self.stdout.write(self.style.SUCCESS("Created Customer (user: customer, pass: customer123)"))

        # 3. Destinations
        dest_bali, _ = Destination.objects.get_or_create(
            name='Bali',
            defaults={
                'country': 'Indonesia',
                'tagline': 'Island of the Gods, Serene Villas & Tropical Beaches',
                'description': 'Discover lush emerald rice terraces, sacred sea temples, luxury beachfront resorts, and world-class spa retreats in Bali.',
                'is_featured': True,
                'is_published': True
            }
        )

        dest_swiss, _ = Destination.objects.get_or_create(
            name='Swiss Alps',
            defaults={
                'country': 'Switzerland',
                'tagline': 'Panoramic Alpine Glaciers & Luxury Mountain Lodges',
                'description': 'Experience breathtaking train journeys across Zermatt and St. Moritz, snow-capped peaks, alpine lakes, and world-renowned ski resorts.',
                'is_featured': True,
                'is_published': True
            }
        )

        dest_japan, _ = Destination.objects.get_or_create(
            name='Tokyo & Kyoto',
            defaults={
                'country': 'Japan',
                'tagline': 'Historic Shrines, Modern Wonders & Culinary Mastery',
                'description': 'Immerse yourself in Japan’s captivating contrast of futuristic cityscapes, bullet trains, ancient temples, and tranquil tea ceremonies.',
                'is_featured': True,
                'is_published': True
            }
        )

        # 4. Travel Packages
        pkg_bali, created = TravelPackage.objects.get_or_create(
            title='5-Day Bali Luxury Villa & Cultural Escape',
            defaults={
                'destination': dest_bali,
                'overview': 'Enjoy 5 days of tropical luxury in private pool villas in Ubud and Seminyak. Includes temple tours, sunset dinner cruise, and spa wellness.',
                'duration_days': 5,
                'duration_nights': 4,
                'price_per_person': 1299.00,
                'inclusions': '4 Nights Luxury Villa Accommodation\nDaily Gourmet Breakfast\nPrivate Airport Transfers\nUbud Monkey Forest & Rice Terrace Tour\nSunset Dinner Cruise at Jimbaran Bay',
                'exclusions': 'International Flight Tickets\nPersonal Travel Insurance\nOptional Water Sports Activities',
                'travel_requirements': 'Passport valid for at least 6 months beyond travel date. Tourist visa available on arrival.',
                'is_featured': True,
                'status': TravelPackage.Status.PUBLISHED,
                'created_by': admin_user
            }
        )
        if created:
            ItineraryDay.objects.create(
                package=pkg_bali,
                day_number=1,
                title='Arrival in Denpasar & Private Villa Transfer',
                description='Meet our private driver at Ngurah Rai International Airport. Transfer to your luxury Ubud villa. Welcome drinks and leisure evening.',
                accommodation='Ubud Luxury Pool Villa',
                meals='Dinner Included',
                transport='Private AC Coach'
            )
            ItineraryDay.objects.create(
                package=pkg_bali,
                day_number=2,
                title='Ubud Cultural Tour & Tegalalang Rice Terraces',
                description='Explore sacred Monkey Forest, Tegallalang Rice Terraces, and traditional art market. Enjoy a traditional Balinese lunch.',
                accommodation='Ubud Luxury Pool Villa',
                meals='Breakfast & Lunch',
                activities='Guided Temple Tour, Swing Experience'
            )
            ItineraryDay.objects.create(
                package=pkg_bali,
                day_number=3,
                title='Transfer to Seminyak & Sunset Beach Dinner',
                description='Check out from Ubud and head to Seminyak coastal resort. Evening romantic seafood dinner at Jimbaran beach.',
                accommodation='Seminyak Beachfront Resort',
                meals='Breakfast & Seafood Dinner'
            )

        pkg_swiss, created = TravelPackage.objects.get_or_create(
            title='7-Day Swiss Alps Scenic Glacier Express',
            defaults={
                'destination': dest_swiss,
                'overview': 'Ride the world-famous Glacier Express train through the heart of the Swiss Alps, staying in Zermatt and Lucerne.',
                'duration_days': 7,
                'duration_nights': 6,
                'price_per_person': 2850.00,
                'inclusions': '6 Nights Premium Hotel Stays\nSwiss Travel Pass 1st Class\nGlacier Express Panoramics Pass\nMount Titlis Excursion',
                'exclusions': 'Personal Meals not mentioned\nSki Equipment Hire',
                'status': TravelPackage.Status.PUBLISHED,
                'is_featured': True,
                'created_by': admin_user
            }
        )

        # 5. Gallery
        cat_island, _ = GalleryCategory.objects.get_or_create(name='Islands & Beaches')
        GalleryImage.objects.get_or_create(
            title='Sunset over Bali Villa Pool',
            defaults={
                'category': cat_island,
                'image': 'gallery/sample_pool.jpg',
                'caption': 'Luxury infinity pool overlooking Balinese jungle',
                'alt_text': 'Balinese tropical resort pool during sunset',
                'is_featured': True
            }
        )

        # 6. Sample Booking Request
        Booking.objects.get_or_create(
            reference_code='JPT-78920',
            defaults={
                'customer': customer_user,
                'guest_name': 'Alex Morgan',
                'guest_email': 'customer@example.com',
                'guest_phone': '+1 555-019-2834',
                'package': pkg_bali,
                'travel_date': datetime.date.today() + datetime.timedelta(days=30),
                'adults_count': 2,
                'children_count': 0,
                'total_quoted_price': 2598.00,
                'status': Booking.Status.PENDING,
                'special_requests': 'Honeymoon arrangement with flower setup.'
            }
        )

        self.stdout.write(self.style.SUCCESS("Database successfully seeded with sample data!"))
