from random import randint

from django.db.utils import IntegrityError
from django.contrib.auth.models import User, Permission
from django.core.management.base import BaseCommand, CommandError

from main.models import Realty, Category, Tag, Saller


class Command(BaseCommand):
    help = """Generates test instances of models:
              Realty, Category, Tag and User from contrib.auth.models.
              Two instances of User will be created automatically"""

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            help='count of categories',
        )
        parser.add_argument(
            "-r",
            help='count of realty',
        )
        parser.add_argument(
            "-t",
            help='count of tags',
        )

    def handle(self, *args, **options):
        try:
            tags_count = int(options['t'])
            categories_count = int(options['c'])
            realty_count = int(options['r'])
        except ValueError as err:
            raise CommandError(self.style.ERROR('Error while parsing commands: %s' % str(err)))

        permissions = [Permission.objects.using("testdb").get(codename="add_realty"),
                       Permission.objects.using("testdb").get(codename="change_realty"),
                       Permission.objects.using("testdb").get(codename="view_realty")]

        tags = [Tag.objects.using("testdb").get_or_create(name=f'testtag_{i}')[0]
                for i in range(1, tags_count+1)]

        categories = [Category.objects.using("testdb").get_or_create(name=f'category_{i}')[0]
                      for i in range(1, categories_count+1)]

        try:
            testuser1 = User.objects.db_manager("testdb").create_user(username="testuser1", password="12345", first_name="Иван", last_name="Иванов")
            testuser1.save()
        except IntegrityError:
            testuser1 = User.objects.db_manager("testdb").get(username="testuser1")

        saller_1 = Saller.objects.using("testdb").get(created_by=testuser1)

        try:
            testuser2 = User.objects.db_manager("testdb").create_user(username="testuser2", password="1234567", first_name="Петр", last_name="Петров")
            testuser2.save()
            testuser2.user_permissions.add(permissions[1])
            testuser2.user_permissions.add(permissions[0])
            testuser2.save()
        except IntegrityError:
            testuser2 = User.objects.db_manager("testdb").get(username="testuser2")

        saller_2 = Saller.objects.using("testdb").get(created_by=testuser2)

        for index in range(1, realty_count+1):
            saller = saller_1 if index % 2 == 0 else saller_2
            category = Category.objects.using("testdb").get(pk=randint(1, categories_count))
            tag = Tag.objects.using("testdb").get(pk=randint(1, tags_count))
            try:
                realty = Realty.objects.using("testdb").create(name=f"name {saller} {category}",
                                    price=12000000, space=75,
                                    description=f"description {saller} {category}",
                                    category=category, saller=saller,
                                    is_mortgage_available=True)
            except IntegrityError:
                realty = Realty.objects.using("testdb").get(name=f"name {saller} {category}")

            realty.tags.set([tag])

            self.stdout.write(self.style.SUCCESS("Succesfully added realty %s" % str(realty)))
