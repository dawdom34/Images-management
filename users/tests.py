from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from .models import ThumbnailSizes, AccountTier


class AccountTests(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(username='admin', password='password123')
        self.admin_data = {'username': 'admin', 'password': 'password123'}
        self.user = get_user_model().objects.create_user(username='user', password='password123')
        self.user_data = {'username': 'user', 'password': 'password123'}
        self.size = ThumbnailSizes.objects.create(size=200)
        self.tier = AccountTier.objects.create(name='Test', original_file=False, expiring_links=False)
        self.tier.thumbnail_size.add(self.size)
        self.login_url = reverse('login')
        self.create_tier_url = reverse('create_tier')
    
    def test_create_user(self):
        user = get_user_model().objects.create_user(username='test', password='password123')
        self.assertEqual(user.username, 'test')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(username='test_admin', password='password123')
        self.assertEqual(user.username, 'test_admin')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_thumbnail_size(self):
        size = ThumbnailSizes.objects.create(size=200)
        self.assertEqual(size.size, 200)

    def test_create_account_tier(self):
        tier = AccountTier.objects.create(name='test_tier', original_file=True, expiring_links=True)
        tier.thumbnail_size.add(self.size)
        self.assertEqual(tier.name,'test_tier')
        self.assertTrue(tier.original_file)
        self.assertTrue(tier.expiring_links)

    def test_user_authentication_success(self):
        response = self.client.post(self.login_url, self.admin_data)
        #print('Token ' + str(response.getvalue()).split(',')[0][12:-1])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_authentication_fail(self):
        invalid_data = {'username': 'invalid', 'password': '123'}
        response = self.client.post(self.login_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_tier_success(self):
        client = APIClient()
        client.post(self.login_url, self.admin_data)
        token = Token.objects.get(user__username='admin')
        
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'name': 'tiertest',
                'thumbnail_size': '200,400',
                'original_file': True,
                'expiring_links': True}
        response = client.post(self.create_tier_url, data=data)
        self.assertEqual(response.content, b'{"detail":"New tier created"}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_tier_with_no_privileges(self):
        client = APIClient()
        client.post(self.login_url, self.user_data)
        token = Token.objects.get(user__username='user')

        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'name': 'tiertest',
                'thumbnail_size': '200,400',
                'original_file': True,
                'expiring_links': True}
        response = client.post(self.create_tier_url, data=data)
        self.assertEqual(response.content, b'{"detail":"Access denied"}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_tier_invalid_data(self):
        client = APIClient()
        client.post(self.login_url, self.admin_data)
        token = Token.objects.get(user__username='admin')
        
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'name': 'testtier12',
                'thumbnail_size': '200,400',
                'original_file': True,
                'expiring_links': True}
        response = client.post(self.create_tier_url, data=data)
        self.assertEqual(response.content, b'{"detail":{"non_field_errors":["Name can contain only letters"]}}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_tier_value_error(self):
        client = APIClient()
        client.post(self.login_url, self.admin_data)
        token = Token.objects.get(user__username='admin')
        
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'name': 'tiertest',
                'thumbnail_size': 'invalid',
                'original_file': True,
                'expiring_links': True}
        response = client.post(self.create_tier_url, data=data)
        self.assertEqual(response.content, b'{"error":"invalid data type for thumbnail_size"}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_tier_size_zero(self):
        client = APIClient()
        client.post(self.login_url, self.admin_data)
        token = Token.objects.get(user__username='admin')
        
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'name': 'tiertest',
                'thumbnail_size': '0,200',
                'original_file': True,
                'expiring_links': True}
        response = client.post(self.create_tier_url, data=data)
        self.assertEqual(response.content, b'{"error":"invalid data type for thumbnail_size"}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    
