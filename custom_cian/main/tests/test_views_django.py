from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase, RequestFactory
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt

from main.models import Category, Realty, Saller, Tag

from main.views import RealtyCreateView, \
                       RealtyDetailView, \
                       RealtyListView, \
                       RealtyUpdateView, \
                       get_common_users_group

from main.forms import RealtyForm, SallerProfileForm


def create_test_data():
    permissions = [Permission.objects.get(codename="add_realty"),
                    Permission.objects.get(codename="change_realty"),
                    Permission.objects.get(codename="view_realty")]

    tags = ["у метро", "вторичка", "от собственника"]

    categories = [Category.objects.create(name=name) for name in
                  ["Квартира", "Офис", "Гараж"]]

    testuser1 = User.objects.create_user(username="testuser1", password="12345", first_name="Иван", last_name="Иванов")
    testuser1.save()
    saller_1 = Saller.objects.get(created_by=testuser1)

    testuser2 = User.objects.create_user(username="testuser2", password="1234567", first_name="Петр", last_name="Петров")
    testuser2.save()
    testuser2.user_permissions.add(permissions[1])
    testuser2.user_permissions.add(permissions[0])
    testuser2.save()
    saller_2 = Saller.objects.get(created_by=testuser2)

    for i, category in enumerate(categories):
        for saller in [saller_1, saller_2]:
            tag = tags[i]
            realty = Realty.objects.create(name=f"name {saller} {category}",
                                    price=12000000, space=75,
                                    description=f"description {saller} {category}",
                                    category=category, saller=saller,
                                    is_mortgage_available=True, tags=[tag])


class TestRealtyListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_test_data()

    def test_get_realty_list(self):
        resp = self.client.get("/realty_list/")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main/realty_list.html')

    def test_failed_get_realty_list(self):
        resp = self.client.get("/realty/")
        self.assertEqual(resp.status_code, 404)

    def test_right_len_list_realty_list(self):
        resp = self.client.get("/realty_list/")
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == False)
        self.assertTrue( len(resp.context['realty_list']) == 6)

    def test_right_len_realty_list_with_tag(self):
        resp = self.client.get("/realty_list/?page=&tag=вторичка")
        self.assertTrue(len(resp.context['realty_list']) == 2)

    def test_fail_get_realty_list_with_wrong_page(self):
        resp = self.client.get("/realty_list/?page=2&tag=вторичка")
        self.assertEqual(resp.status_code, 404)


class TestRealtyDetailView(TestCase):

    def setUp(self):
        create_test_data()

    def test_fail_get_realty(self):
        resp = self.client.get("/realty_list/2/")
        self.assertEqual(resp.status_code, 404)

    def test_get_right_realty(self):
        resp = self.client.get("/realty_list/name-ivan-ivanov-kvartira/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["object"], Realty.objects.get(pk=1))
        self.assertTemplateUsed(resp, 'main/realty_detail.html')


class TestRealtyUpdateView(TestCase):

    def setUp(self):
        create_test_data()

    def test_logged_in_with_permission_denied(self):
        login = self.client.login(username="testuser1", password="12345")
        resp = self.client.get("/realty_list/name-ivan-ivanov-kvartira/edit")
        self.assertEqual(resp.status_code, 403)

    def test_get_update_form(self):
        login = self.client.login(username="testuser2", password="1234567")
        resp = self.client.get("/realty_list/name-petr-petrov-kvartira/edit")
        realty = Realty.objects.get(slug="name-petr-petrov-kvartira")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(isinstance(resp.context["form"], RealtyForm))
        self.assertEqual(resp.context["form"].initial["name"], realty.name)
        self.assertTemplateUsed(resp, 'main/realty_form.html')

    def test_redirect_logout(self):
        resp = self.client.get("/realty_list/name-petr-petrov-kvartira/edit")
        self.assertEqual(resp.status_code,302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))


class TestRealtyCreateView(TestCase):

    def setUp(self):
        create_test_data()

    def test_redirect_logout(self):
        resp = self.client.get("/realty/add/")
        self.assertEqual(resp.status_code,302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_logged_in_with_permission_denied(self):
        login = self.client.login(username="testuser1", password="12345")
        resp = self.client.get("/realty/add/")
        self.assertEqual(resp.status_code, 403)

    def test_get_realty_form(self):
        login = self.client.login(username="testuser2", password="1234567")
        resp = self.client.get("/realty/add/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(isinstance(resp.context["form"], RealtyForm))
        self.assertTemplateUsed(resp, 'main/realty_form.html')

    def test_successful_create_realty(self):
        login = self.client.login(username="testuser2", password="1234567")
        form_data = {
            "name": "test Realty",
            "price": 1000,
            "space": 20,
            "description": "test description",
            "tags": ["вторичка"],
            "category": 1,
            "saller": 2,
            "is_mortgage_available": "on",
            "counter": 0
        }
        resp = self.client.post("/realty/add/", form_data)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, "/realty_list/test-realty/")
        self.assertTrue(Realty.objects.get(name="test Realty"))


class SallerUpdateView(TestCase):

    def setUp(self):
        create_test_data()

    def test_get_update_form(self):
        login = self.client.login(username="testuser1", password="12345")
        resp = self.client.get("/accounts/profile/1/")
        saller = Saller.objects.get(created_by__username="testuser1")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main/saller_update_form.html')
        self.assertTrue(isinstance(resp.context["form"], SallerProfileForm))
        self.assertEqual(resp.context["form"].initial["first_name"], saller.first_name)

    def test_logged_in_with_permission_denied(self):
        login = self.client.login(username="testuser2", password="1234567")
        resp = self.client.get("/accounts/profile/1/")
        self.assertEqual(resp.status_code, 403)

    def test_redirect_logout(self):
        resp = self.client.get("/accounts/profile/1/")
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))
