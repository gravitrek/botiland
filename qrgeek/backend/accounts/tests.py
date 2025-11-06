"""
Tests for accounts app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import SubscriptionPlan, UserSubscription
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class UserModelTest(TestCase):
    """Tests for User model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_user_creation(self):
        """Test user can be created."""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_str(self):
        """Test user string representation."""
        self.assertEqual(str(self.user), 'test@example.com')

    def test_qr_code_limit(self):
        """Test QR code limit property."""
        self.assertEqual(self.user.qr_code_limit, 5)  # Default free plan


class SubscriptionPlanModelTest(TestCase):
    """Tests for SubscriptionPlan model."""

    def setUp(self):
        self.plan = SubscriptionPlan.objects.create(
            name='Test Plan',
            slug='test-plan',
            price=9.99,
            billing_period='monthly',
            qr_limit=25,
            scan_limit=5000
        )

    def test_plan_creation(self):
        """Test plan can be created."""
        self.assertEqual(self.plan.name, 'Test Plan')
        self.assertEqual(self.plan.price, 9.99)

    def test_plan_str(self):
        """Test plan string representation."""
        expected = "Test Plan - $9.99/monthly"
        self.assertEqual(str(self.plan), expected)


class UserRegistrationAPITest(APITestCase):
    """Tests for user registration API."""

    def test_register_user(self):
        """Test user can register."""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)

    def test_register_password_mismatch(self):
        """Test registration fails with password mismatch."""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'testpass123',
            'password_confirm': 'differentpass'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        """Test registration fails with duplicate email."""
        User.objects.create_user(
            email='existing@example.com',
            username='existing',
            password='testpass123'
        )
        data = {
            'email': 'existing@example.com',
            'username': 'newuser',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginAPITest(APITestCase):
    """Tests for user login API."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_login_success(self):
        """Test user can login."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        """Test login fails with invalid credentials."""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileAPITest(APITestCase):
    """Tests for user profile API."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        """Test user can get their profile."""
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_update_profile(self):
        """Test user can update their profile."""
        data = {
            'full_name': 'Test User',
            'company_name': 'Test Company'
        }
        response = self.client.put('/api/auth/profile/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Test User')
