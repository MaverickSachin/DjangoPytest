import pytest
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser
from ..views import product_details, index
from django.test import TestCase


@pytest.mark.django_db
class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()
        mixer.blend('products.Product')
        cls.factory = RequestFactory()

    def test_index_view(self):
        path = reverse("products:index")
        request = self.factory.get(path)

        response = index(request)
        assert response.status_code == 200

    def test_product_details_authenticated(self):

        path = reverse("products:detail", kwargs={'pk': 1})
        request = self.factory.get(path)
        request.user = mixer.blend(User)

        response = product_details(request, pk=1)
        assert response.status_code == 200

    def test_product_details_unauthenticated(self):

        path = reverse("products:detail", kwargs={'pk': 1})
        request = self.factory.get(path)
        request.user = AnonymousUser()

        response = product_details(request, pk=1)
        assert 'accounts/login' in response.url
