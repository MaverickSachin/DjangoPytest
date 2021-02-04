import pytest
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser
from ..views import product_details, index
from django.test import TestCase


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture
def product(db):
    return mixer.blend('products.Product')


def test_index_view(factory):
    path = reverse("products:index")
    request = factory.get(path)

    response = index(request)
    assert response.status_code == 200

def test_product_details_authenticated(factory, product):

    mixer.blend('products.Product')

    path = reverse("products:detail", kwargs={'pk': 1})
    request = factory.get(path)
    request.user = mixer.blend(User)

    response = product_details(request, pk=1)
    assert response.status_code == 200

def test_product_details_unauthenticated(factory, product):

    mixer.blend('products.Product')

    path = reverse("products:detail", kwargs={'pk': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = product_details(request, pk=1)
    assert 'accounts/login' in response.url
