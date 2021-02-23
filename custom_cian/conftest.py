import pytest
from main.models import Category, Realty, Saller, Tag
from django.contrib.auth.models import Permission


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture()
def logged_user(django_user_model):
    permissions = [Permission.objects.get(codename="add_realty"),
                Permission.objects.get(codename="change_realty"),
                Permission.objects.get(codename="view_realty")]
    user = django_user_model.objects.create(
        username='testuser1', password='12345'
    )
    user.user_permissions.add(permissions[0])
    user.user_permissions.add(permissions[1])
    user.save()
    return user


@pytest.fixture()
def user_without_perms(django_user_model):
    user = django_user_model.objects.create(
        username='testuser2', password='1234567'
    )
    return user


@pytest.fixture()
def saller(logged_user):
    return Saller.objects.get(created_by=logged_user)


@pytest.fixture()
def category():
    return Category.objects.create(name='Category 1')

@pytest.fixture()
def tag():
    return Tag.objects.create(name="test_tag")


@pytest.fixture()
def realty(saller, category):
    realty = Realty.objects.create(name=f"name {saller} {category}",
                                    price=12000000, space=75,
                                    description=f"description {saller} {category}",
                                    category=category, saller=saller,
                                    is_mortgage_available=True)
    return realty
