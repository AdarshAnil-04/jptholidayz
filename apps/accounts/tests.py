from django.test import TestCase
from django.urls import reverse
from .models import User, CustomerProfile

class AccountModelAndRBACTests(TestCase):
    def test_create_customer_user(self):
        user = User.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='Password123!',
            role=User.Role.CUSTOMER
        )
        CustomerProfile.objects.create(user=user)
        self.assertEqual(user.role, User.Role.CUSTOMER)
        self.assertTrue(user.is_customer)
        self.assertFalse(user.is_booking_staff)

    def test_create_staff_user(self):
        staff = User.objects.create_user(
            username='teststaff',
            email='staff@test.com',
            password='Password123!',
            role=User.Role.BOOKING_STAFF,
            is_staff=True
        )
        self.assertTrue(staff.is_booking_staff)
        self.assertFalse(staff.is_admin_owner)

    def test_registration_view(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
