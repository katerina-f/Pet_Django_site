from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase, RequestFactory
from django.contrib.contenttypes.models import ContentType

from main.models import Category, Realty, Saller, Tag

from main.views import RealtyCreateView, \
                       RealtyDetailView, \
                       RealtyListView, \
                       RealtyUpdateView, \
                       get_common_users_group

from main.forms import RealtyForm


def create_test_data():
    permissions = [Permission.objects.get(codename="add_realty"),
                    Permission.objects.get(codename="change_realty"),
                    Permission.objects.get(codename="view_realty")]

    tags = [Tag.objects.create(name=name) for name in
            ["у метро", "вторичка", "от собственника"]]

    categories = [Category.objects.create(name=name) for name in
                  ["Квартира", "Офис", "Гараж"]]

    testuser1 = User.objects.create_user(username="testuser1", password="12345", first_name="Иван", last_name="Иванов")
    testuser1.save()
    saller_1 = Saller.objects.get(created_by=testuser1)

    testuser2 = User.objects.create_user(username="testuser2", password="1234567", first_name="Петр", last_name="Петров")
    testuser2.save()
    testuser2.user_permissions.add(permissions[1])
    testuser2.save()
    saller_2 = Saller.objects.get(created_by=testuser2)

    for i, category in enumerate(categories):
        for saller in [saller_1, saller_2]:
            realty = Realty.objects.create(name=f"name {saller} {category}",
                                    price=12000000, space=75,
                                    description=f"description {saller} {category}",
                                    category=category, saller=saller,
                                    is_mortgage_available=True)

            tag = Tag.objects.get(pk=i+1)
            realty.tags.set([tag])


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
