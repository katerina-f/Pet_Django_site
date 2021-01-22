from django.db import models


class Realty(models.Model):

    name = models.CharField(verbose_name='Название', max_length=100)
    price = models.IntegerField(verbose_name='Цена')
    space = models.IntegerField(verbose_name='Площадь')
    published_at = models.DateField(verbose_name='Дата публикации', auto_now_add=True)
    description = models.TextField(verbose_name='Описание')
    tags = models.ManyToManyField(Tag, related_name="Тэги")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    saller = models.ForeignKey(Saller, on_delete=CASCADE)
    slug = models.SlugField(verbose_name='Ссылка', max_length=100)

    def __str__(self):
        return self.name


class Saller(models.Model):

    first_name = models.CharField(verbose_name="Имя", max_length=50)
    last_name = models.CharField(verbose_name="Фамилия", max_length=50)
    registered_at = models.DateField(verbose_name="Дата регистрации", auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):

    name = models.CharField(verbose_name='Название', max_length=100)
    slug = models.SlugField(verbose_name='Ссылка', max_length=100)


class Tag(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    slug = models.SlugField(verbose_name='Ссылка', max_length=100)
    realty_list = models.ManyToManyField(Realty, related_name="Список недвижимости")
