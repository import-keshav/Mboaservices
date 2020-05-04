import unittest
from django.urls import reverse
from django.test import Client
from .models import User
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_user(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["email"] = "email"
    defaults["mobile"] = "mobile"
    defaults["password"] = "password"
    defaults["avatar"] = "avatar"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


class UserViewTest(unittest.TestCase):
    '''
    Tests for User
    '''
    def setUp(self):
        self.client = Client()

    def test_list_user(self):
        url = reverse('user_user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        url = reverse('user_user_create')
        data = {
            "name": "name",
            "email": "email",
            "mobile": "mobile",
            "password": "password",
            "avatar": "avatar",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_user(self):
        user = create_user()
        url = reverse('user_user_detail', args=[user.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        user = create_user()
        data = {
            "name": "name",
            "email": "email",
            "mobile": "mobile",
            "password": "password",
            "avatar": "avatar",
        }
        url = reverse('user_user_update', args=[user.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


