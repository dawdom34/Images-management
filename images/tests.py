from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse

from users.models import ThumbnailSizes, AccountTier, Account

from .models import Image
from .serializers import OriginalImageSerializer

from PIL import Image as PILimage
import io


class ImageTests(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(username='admin', password='password123')
        self.admin_data = {'username': 'admin', 'password': 'password123'}
        self.user = get_user_model().objects.create_user(username='user', password='password123')
        self.user_data = {'username': 'user', 'password': 'password123'}
        self.size = ThumbnailSizes.objects.create(size=200)
        self.tier = AccountTier.objects.create(name='Test', original_file=True, expiring_links=True)
        self.tier2 = AccountTier.objects.create(name='Testtest', original_file=False, expiring_links=False)
        self.tier.thumbnail_size.add(self.size)
        self.admin = Account.objects.get(id=self.admin_user.id)
        self.admin.account_tier = self.tier
        self.user = Account.objects.get(id=self.user.id)
        self.user.account_tier = self.tier2
        self.image_path = '../image_test/test_image.png'
        self.image = Image.objects.create(owner=self.admin_user, image=self.image_path)
        self.image = Image.objects.create(owner=self.user, image=self.image_path)
        self.login_url = reverse('login')
        self.create_tier_url = reverse('create_tier')
        # URLS
        self.img_save_url = reverse('image_save')
        self.list_images_url = reverse('list_images')
        self.original_image_url = reverse('get_original_file')
        self.get_thumbnail_url = reverse('get_thumbnail')

    def generate_image(self):
        file = io.BytesIO()
        image = PILimage.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_image_save_success(self):
        client = APIClient()
        client.post(self.login_url, self.admin_data)
        token = Token.objects.get(user__username='admin')
        data = {'owner': self.admin_user.id, 'image': self.generate_image()}
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(self.img_save_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.content, b'{"detail":"Image saved"}')

    def test_image_fail(self):
        client = APIClient()
        client.post(self.login_url, self.admin_data)
        token = Token.objects.get(user__username='admin')
        data = {'owner': self.admin_user.id, 'image': ''}
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(self.img_save_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_images(self):
        client = APIClient()
        client.post(self.login_url, self.admin_data)
        token = Token.objects.get(user__username='admin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(self.list_images_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_original_file_success(self):
        client = APIClient()
        client.post(self.login_url, self.admin_data)
        token = Token.objects.get(user__username='admin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'id': self.image.id}
        response = client.get(self.original_image_url, data=data)
        self.assertEqual(response.content, '')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_original_file_invalid_id(self):
        client = APIClient()
        client.post(self.login_url, self.admin_data)
        token = Token.objects.get(user__username='admin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'id': 123}
        response = client.get(self.original_image_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, '')

    def test_original_file_no_permissions(self):
        client = APIClient()
        client.post(self.login_url, self.user_data)
        token = Token.objects.get(user__username='user')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'id': self.image.id}
        response = client.get(self.original_image_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, '')

    def test_get_thumbnail_success(self):
        client = APIClient()
        client.post(self.login_url, self.admin_data)
        token = Token.objects.get(user__username='admin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'image_id': self.image.id, 'size': 200,}
        response = client.get(self.get_thumbnail_url, data=data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_thumbnail_id_not_exist(self):
        client = APIClient()
        client.post(self.login_url, self.admin_data)
        token = Token.objects.get(user__username='admin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'image_id': 123, 'size': 200}
        response = client.get(self.get_thumbnail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_thumbnail_access_denied(self):
        client = APIClient()
        client.post(self.login_url, self.admin_data)
        token = Token.objects.get(user__username='admin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'image_id': 123, 'size': 400}
        response = client.get(self.get_thumbnail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_serializer(self):
        data = {'id': self.image.id}
        ser = OriginalImageSerializer(data=data)
        print(f'++++++++++++++++++++++++{ser.is_valid()}')