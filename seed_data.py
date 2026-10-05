import os
import urllib.request
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jpt_holidays.settings')
django.setup()

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from apps.accounts.models import User, CustomerProfile
from apps.destinations.models import Destination
from apps.packages.models import TravelPackage
from apps.bookings.models import Booking
from apps.enquiries.models import CustomEnquiry

import tempfile

def download_image(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()
            tf = tempfile.NamedTemporaryFile(delete=False)
            tf.write(data)
            tf.flush()
            tf.close()
            return tf.name
    except Exception as e:
        print(f"Failed to download image {url}: {e}")
        return None

def seed_users():
    print("Seeding dummy customer accounts...")
    customers_data = [
        {
            'username': 'sarah_jenkins',
            'first_name': 'Sarah',
            'last_name': 'Jenkins',
            'email': 'sarah.jenkins@example.com',
            'phone': '+1 (555) 234-5678',
            'address': '124 Maple Street, San Francisco, CA',
            'preferences': 'Loves luxury beach resorts, vegan dining, and ocean views.'
        },
        {
            'username': 'alex_rivera',
            'first_name': 'Alex',
            'last_name': 'Rivera',
            'email': 'alex.rivera@example.com',
            'phone': '+1 (555) 876-5432',
            'address': '89 Ocean Drive, Miami, FL',
            'preferences': 'High-adventure hiking, wildlife tours, and cultural photography.'
        },
        {
            'username': 'david_chen',
            'first_name': 'David',
            'last_name': 'Chen',
            'email': 'david.chen@example.com',
            'phone': '+1 (555) 345-6789',
            'address': '452 Pine Terrace, Seattle, WA',
            'preferences': 'Alpine skiing, luxury train travel, fine dining experiences.'
        },
        {
            'username': 'emily_watson',
            'first_name': 'Emily',
            'last_name': 'Watson',
            'email': 'emily.watson@example.com',
            'phone': '+44 20 7946 0912',
            'address': '12 Kensington Gardens, London, UK',
            'preferences': 'Honeymoon luxury suites, spa wellness retreats, private yacht charters.'
        },
        {
            'username': 'michael_brown',
            'first_name': 'Michael',
            'last_name': 'Brown',
            'email': 'michael.brown@example.com',
            'phone': '+1 (555) 901-2345',
            'address': '789 Broadway Ave, New York, NY',
            'preferences': 'Family-friendly guided excursions, private transfers, beach villas.'
        },
    ]

    for data in customers_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'phone': data['phone'],
                'role': User.Role.CUSTOMER,
                'is_active': True,
            }
        )
        if created:
            user.set_password('Password123!')
            user.save()
            print(f"  [+] Created customer user: {user.username} (Password: Password123!)")
        else:
            print(f"  [*] Customer user exists: {user.username}")

        profile, p_created = CustomerProfile.objects.get_or_create(user=user)
        profile.address = data['address']
        profile.travel_preferences = data['preferences']
        profile.save()

def seed_destinations_and_packages():
    print("Seeding destinations and packages with images...")
    dest_data = [
        {
            'name': 'Bali',
            'country': 'Indonesia',
            'tagline': 'Tropical Island Paradise & Cultural Retreat',
            'description': 'Experience lush rice terraces, sacred sea temples, world-class beach resorts, and rejuvenating holistic wellness in Bali.',
            'image_url': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
        },
        {
            'name': 'Swiss Alps',
            'country': 'Switzerland',
            'tagline': 'Majestic Peaks & Alpine Luxury Escapes',
            'description': 'Marvel at the iconic Matterhorn, ride scenic panorama trains like the Glacier Express, and indulge in luxury mountain chalets.',
            'image_url': 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
        },
        {
            'name': 'Tokyo & Kyoto',
            'country': 'Japan',
            'tagline': 'Historic Shrines & Neon Metropolis',
            'description': 'Witness ancient bamboo groves, majestic Shinto shrines, Michelin-starred cuisine, and high-speed bullet train journeys.',
            'image_url': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
        },
        {
            'name': 'Maldives',
            'country': 'Indian Ocean',
            'tagline': 'Overwater Bungalows & Crystal Coral Lagoons',
            'description': 'Escape to turquoise lagoons, private island resorts, underwater dining, and pristine white sand beaches in absolute luxury.',
            'image_url': 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
        },
        {
            'name': 'Serengeti National Park',
            'country': 'Tanzania',
            'tagline': 'Unrivaled Wildlife Safaris & Luxury Tented Camps',
            'description': 'Witness the Great Migration, majestic lion prides, hot air balloon safaris at sunrise, and authentic wilderness hospitality.',
            'image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
        },
    ]

    dest_objs = {}
    for d in dest_data:
        dest, created = Destination.objects.get_or_create(
            name=d['name'],
            defaults={
                'country': d['country'],
                'tagline': d['tagline'],
                'description': d['description'],
                'is_featured': d['is_featured'],
                'is_published': True,
            }
        )
        if not dest.cover_image:
            img_path = download_image(d['image_url'])
            if img_path:
                with open(img_path, 'rb') as f:
                    dest.cover_image.save(f"{dest.slug}.jpg", File(f), save=True)
                os.remove(img_path)
                print(f"  [+] Saved image for destination: {dest.name}")
        dest_objs[d['name']] = dest

    packages_data = [
        {
            'title': '5-Day Bali Luxury Villa & Island Escape',
            'destination': dest_objs['Bali'],
            'price': 1499.00,
            'duration_days': 5,
            'duration_nights': 4,
            'overview': 'Indulge in a private pool villa in Seminyak, private guided temple tours to Tanah Lot and Ubud, and sunset catamaran cruises.',
            'inclusions': '4 Nights Luxury Pool Villa Accommodation\nDaily Buffet Breakfast & Welcome Cocktail\nAirport Private Round-trip Transfers\nGuided Ubud & Tanah Lot Cultural Excursions',
            'exclusions': 'International Flights\nPersonal Expenses & Gratuities\nTravel Insurance',
            'image_url': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
        },
        {
            'title': '7-Day Swiss Alps Scenic Express & Resort',
            'destination': dest_objs['Swiss Alps'],
            'price': 2850.00,
            'duration_days': 7,
            'duration_nights': 6,
            'overview': 'Ride the legendary Glacier Express train across breathtaking alpine pass panoramas and stay at 5-star mountain resorts in Zermatt and St. Moritz.',
            'inclusions': '6 Nights 5-Star Hotel Accommodation\nFirst Class Glacier Express Train Pass\nDaily Gourmet Breakfast & Alpine Dinners\nMount Titlis Cable Car Excursion Pass',
            'exclusions': 'Personal Ski Equipment Rentals\nInternational Airfare\nVisa Processing Fees',
            'image_url': 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
        },
        {
            'title': '8-Day Tokyo & Kyoto Cultural Immersion',
            'destination': dest_objs['Tokyo & Kyoto'],
            'price': 3200.00,
            'duration_days': 8,
            'duration_nights': 7,
            'overview': 'Immerse yourself in Japan contrasts: high-speed Shinkansen trains, private tea ceremonies in Kyoto, traditional Ryokan hot spring baths, and vibrant Tokyo nightlife.',
            'inclusions': '7 Nights Luxury Hotel & Ryokan Stay\n7-Day Ordinary Japan Rail Bullet Train Pass\nPrivate Kyoto Tea Ceremony & Gion Walking Tour\nEnglish Speaking Local Tour Escort',
            'exclusions': 'Personal Souvenirs & Alcoholic Beverages\nInternational Airfare',
            'image_url': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
        },
        {
            'title': '6-Day Maldives Overwater Villa Sanctuary',
            'destination': dest_objs['Maldives'],
            'price': 3999.00,
            'duration_days': 6,
            'duration_nights': 5,
            'overview': 'Unwind in a secluded overwater ocean villa with private plunge pool, glass-floor viewing panels, sunset dolphin cruises, and underwater reef snorkeling.',
            'inclusions': '5 Nights Luxury Overwater Villa Stay\nSeaplane Airport Round-trip Transfers\nFull Board Dining & Selected Beverages\nSunset Dolphin Cruise & Snorkeling Gear',
            'exclusions': 'Scuba Diving Certification Courses\nSpa Treatments Outside Package',
            'image_url': 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
        },
        {
            'title': '7-Day Serengeti Wildlife Safari & Luxury Camp',
            'destination': dest_objs['Serengeti National Park'],
            'price': 4150.00,
            'duration_days': 7,
            'duration_nights': 6,
            'overview': 'Experience world-class wildlife viewing across Ngorongoro Crater and Serengeti plains with private 4x4 land cruisers and luxury canvas tented camps.',
            'inclusions': '6 Nights Luxury Safari Lodge & Tented Camp\nPrivate 4x4 Custom Safari Vehicle & Expert Guide\nAll National Park Entry & Conservation Fees\nFull Board Meals & Bush Dinners',
            'exclusions': 'Hot Air Balloon Safari Add-on\nInternational Flights & Visas',
            'image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
        },
    ]

    for p in packages_data:
        pkg, created = TravelPackage.objects.get_or_create(
            title=p['title'],
            defaults={
                'destination': p['destination'],
                'price_per_person': p['price'],
                'duration_days': p['duration_days'],
                'duration_nights': p['duration_nights'],
                'overview': p['overview'],
                'inclusions': p['inclusions'],
                'exclusions': p['exclusions'],
                'is_featured': p['is_featured'],
                'status': TravelPackage.Status.PUBLISHED,
            }
        )
        if not pkg.cover_image:
            img_path = download_image(p['image_url'])
            if img_path:
                with open(img_path, 'rb') as f:
                    pkg.cover_image.save(f"{pkg.slug}.jpg", File(f), save=True)
                os.remove(img_path)
                print(f"  [+] Saved image for package: {pkg.title}")

if __name__ == '__main__':
    seed_users()
    seed_destinations_and_packages()
    print("Seeding complete successfully!")
