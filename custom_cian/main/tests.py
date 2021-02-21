from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase, RequestFactory

from main.models import Category, Realty, Saller, Tag

from main.views import RealtyCreateView, \
                       RealtyDetailView, \
                       RealtyListView, \
                       RealtyUpdateView, \
                       get_common_users_group


class TestRealtyListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        tags = [Tag.objects.create(name=name) for name in
                     ["у метро", "вторичка", "от собственника"]]

        categories = [Category.objects.create(name=name) for name in
                           ["Квартира", "Офис", "Гараж"]]

        testuser1 = User.objects.create_user(username="testuser1", password="12345")
        testuser1.save()
        saller_1 = Saller.objects.create(first_name="Иван", last_name="Иванов", created_by=testuser1)

        testuser2 = User.objects.create_user(username="testuser2", password="1234567")
        testuser2.save()
        saller_2 = Saller.objects.create(first_name="Петр", last_name="Петров", created_by=testuser2)

        for i, category in enumerate(categories):
            for saller in [saller_1, saller_2]:
                tag = Tag.objects.get(pk=i+1)
                realty = Realty.objects.create(name=f"name {saller} {category}",
                                        price=12000000, space=75,
                                        description=f"description {saller} {category}",
                                        category=category, saller=saller,
                                        is_mortgage_available=True)
                realty.tags.set([tag])

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

        self.categories = [Category.objects.create(name=name) for name in
                           ["Квартира", "Офис", "Гараж"]]

        self.testuser1 = User.objects.create_user(username="testuser1", password="12345")
        self.testuser1.save()
        self.saller_1 = Saller.objects.create(first_name="Иван", last_name="Иванов", created_by=self.testuser1)

        self.testuser2 = User.objects.create_user(username="testuser2", password="1234567")
        self.testuser2.save()
        self.testuser2.groups.add(get_common_users_group())
        self.saller_2 = Saller.objects.create(first_name="Петр", last_name="Петров", created_by=self.testuser2)

        for category in self.categories:
            for saller in [self.saller_1, self.saller_2]:
                Realty.objects.create(name=f"name {saller} {category}",
                                        price=12000000, space=75,
                                        description=f"description {saller} {category}",
                                        category=category, saller=saller,
                                        is_mortgage_available=True)

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
        # common_users = Group.objects.create(name="common_users")
        # common_users.permissions.set(list(Permission.objects.filter(codename__icontains="saller").exclude(codename__startswith="delete")))

        self.tags = [Tag.objects.create(name=name) for name in
                     ["у метро", "вторичка", "от собственника"]]

        self.categories = [Category.objects.create(name=name) for name in
                           ["Квартира", "Офис", "Гараж"]]

        self.testuser1 = User.objects.create_user(username="testuser1", password="12345")
        self.testuser1.save()
        # self.testuser1.groups.add(common_users)

        self.saller_1 = Saller.objects.create(first_name="Иван", last_name="Иванов", created_by=self.testuser1)

        self.testuser2 = User.objects.create_user(username="testuser2", password="1234567")
        self.testuser2.save()
        self.testuser2.groups.add(get_common_users_group())
        self.saller_2 = Saller.objects.create(first_name="Петр", last_name="Петров", created_by=self.testuser2)

        for i, category in enumerate(self.categories):
            for saller in [self.saller_1, self.saller_2]:
                realty = Realty.objects.create(name=f"name {saller} {category}",
                                        price=12000000, space=75,
                                        description=f"description {saller} {category}",
                                        category=category, saller=saller,
                                        is_mortgage_available=True)

                tag = Tag.objects.get(pk=i+1)
                realty.tags.set([tag])

    def test_fail_get_update_form(self):
        login = self.client.login(username="testuser1", password="12345")
        resp = self.client.get("/realty_list/name-ivan-ivanov-kvartira/edit")
        self.assertEqual(resp.status_code, 403)
