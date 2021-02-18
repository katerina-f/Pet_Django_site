from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from main.models import Category, Realty, Saller, Tag

from main.views import RealtyCreateView, \
                       RealtyDetailView, \
                       RealtyListView, \
                       RealtyUpdateView


User = get_user_model()


class TestRealtyBehavior(TestCase):

    def setUp(self):
        self.tags = [Tag.objects.create(name=name) for name in
                     ["у метро", "вторичка", "от собственника"]]

        self.categories = [Category.objects.create(name=name) for name in
                           ["Квартира", "Офис", "Гараж"]]

        self.user = User.objects.create(username="test", password="test")
        self.saller = Saller.objects.create(first_name="Иван", last_name="Иванов", created_by=self.user)

        self.realty = Realty.objects.create(name="Двухкомнатная квартира с видом на парк",
                                            price=12000000, space=75,
                                            description="Просторная квартира с окнами выходящими в парк, \
                                                в пешей доступности метро, торговые центры",
                                            category=self.categories[0], saller=self.saller,
                                            is_mortgage_available=True)
        self.factory = RequestFactory()

    def test_get_realty(self):
        get = self.factory.get("/realty/")
        response = RealtyDetailView.as_view().get(get, pk=1)
        self.assertEqual(response.status_code, 200)
