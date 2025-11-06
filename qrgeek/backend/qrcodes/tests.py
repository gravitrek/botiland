"""
Tests for qrcodes app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import QRCode, Tag
from .utils import encode_vcard, encode_wifi, encode_email

User = get_user_model()


class QRCodeModelTest(TestCase):
    """Tests for QRCode model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.qr_code = QRCode.objects.create(
            user=self.user,
            name='Test QR',
            qr_type='url',
            content={'url': 'https://example.com'}
        )

    def test_qr_code_creation(self):
        """Test QR code can be created."""
        self.assertEqual(self.qr_code.name, 'Test QR')
        self.assertEqual(self.qr_code.qr_type, 'url')
        self.assertTrue(len(self.qr_code.short_code) > 0)

    def test_short_url_generation(self):
        """Test short URL is generated."""
        self.assertIn(self.qr_code.short_code, self.qr_code.short_url)

    def test_increment_scan(self):
        """Test scan counter incrementation."""
        initial_scans = self.qr_code.total_scans
        self.qr_code.increment_scan()
        self.assertEqual(self.qr_code.total_scans, initial_scans + 1)


class UtilsTest(TestCase):
    """Tests for QR code utility functions."""

    def test_encode_vcard(self):
        """Test vCard encoding."""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890',
            'email': 'john@example.com'
        }
        vcard = encode_vcard(data)
        self.assertIn('BEGIN:VCARD', vcard)
        self.assertIn('John Doe', vcard)
        self.assertIn('END:VCARD', vcard)

    def test_encode_wifi(self):
        """Test WiFi encoding."""
        data = {
            'ssid': 'MyNetwork',
            'password': 'password123',
            'security_type': 'WPA'
        }
        wifi = encode_wifi(data)
        self.assertIn('WIFI:', wifi)
        self.assertIn('MyNetwork', wifi)

    def test_encode_email(self):
        """Test email encoding."""
        data = {
            'to': 'test@example.com',
            'subject': 'Test Subject',
            'body': 'Test Body'
        }
        email = encode_email(data)
        self.assertIn('mailto:', email)
        self.assertIn('test@example.com', email)


class QRCodeAPITest(APITestCase):
    """Tests for QR code API."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_qr_code(self):
        """Test QR code creation via API."""
        data = {
            'name': 'Test QR',
            'qr_type': 'url',
            'content': {'url': 'https://example.com'}
        }
        response = self.client.post('/api/qr/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test QR')

    def test_list_qr_codes(self):
        """Test listing QR codes."""
        QRCode.objects.create(
            user=self.user,
            name='Test QR 1',
            qr_type='url',
            content={'url': 'https://example.com'}
        )
        response = self.client.get('/api/qr/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_qr_code_detail(self):
        """Test getting QR code details."""
        qr_code = QRCode.objects.create(
            user=self.user,
            name='Test QR',
            qr_type='url',
            content={'url': 'https://example.com'}
        )
        response = self.client.get(f'/api/qr/{qr_code.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test QR')

    def test_update_qr_code(self):
        """Test updating QR code."""
        qr_code = QRCode.objects.create(
            user=self.user,
            name='Test QR',
            qr_type='url',
            content={'url': 'https://example.com'}
        )
        data = {'name': 'Updated QR'}
        response = self.client.patch(f'/api/qr/{qr_code.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated QR')

    def test_delete_qr_code(self):
        """Test deleting QR code."""
        qr_code = QRCode.objects.create(
            user=self.user,
            name='Test QR',
            qr_type='url',
            content={'url': 'https://example.com'}
        )
        response = self.client.delete(f'/api/qr/{qr_code.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(QRCode.objects.filter(id=qr_code.id).exists())


class TagAPITest(APITestCase):
    """Tests for Tag API."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_tag(self):
        """Test tag creation."""
        data = {'name': 'Test Tag', 'slug': 'test-tag'}
        response = self.client.post('/api/qr/tags/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_tags(self):
        """Test listing tags."""
        Tag.objects.create(user=self.user, name='Tag 1', slug='tag-1')
        response = self.client.get('/api/qr/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
