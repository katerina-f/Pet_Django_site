from pytils import dt, translit

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Realty(models.Model):
    """
    Класс, описывающий модель объекта недвижимости
    :param name: Название объекта
    :param price: Цена объекта
    :param space: Площадь объекта
    :param published_at: Дата публикации (заполняется автоматически при создании)
    :param description: Детальное описание объекта
    :param tags: Тэги для объекта
    :param category: Категория, к которой относится объект
    :param saller: Продавец, создающий объект
    :param slug: Репрезентация части url адреса для объекта
                 (заполняется автоматически при создании)
    :param is_mortgage_available: Доступность ипотеки
    :param counter: Счетчик просмотров объекта
                    (заполняется автоматически)
    """

    name = models.CharField(verbose_name='Название', max_length=100, unique=True)
    price = models.IntegerField(verbose_name='Цена')
    space = models.IntegerField(verbose_name='Площадь')
    published_at = models.DateField(verbose_name='Дата публикации', auto_now_add=True)
    description = models.TextField(verbose_name='Описание')
    tags = models.ManyToManyField('Tag', related_name="tags")
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    saller = models.ForeignKey('Saller', on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='Ссылка', max_length=100, null=True)
    is_mortgage_available = models.BooleanField(verbose_name="Возможность ипотеки", blank=False)
    counter = models.IntegerField(verbose_name="Количество просмотров", default=0)
    in_archive = models.BooleanField(verbose_name="В архиве", default=False)

    class Meta:
        verbose_name = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"
        ordering = ["-published_at"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("realty_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs) -> None:
        self.slug = translit.slugify(f"{self.name}")
        super(Realty, self).save(*args, **kwargs)

    def published_at_ru(self) -> str:
        """ Метод для перевода даты публикации в русскоязычный формат """
        return dt.ru_strftime(u"%d %B %Y", self.published_at, inflected=True)


class Saller(models.Model):
    """
    Класс, описывающий модель продавца
    :param first_name: Имя продавца
    :param last_name: Фамилия продавца
    :param registered_at: Дата регистрации (заполняется автоматически при создании)
    :param created_by: объект пользователя (User), который создал профиль
    :param email: email адрес продавца
    """
    first_name = models.CharField(verbose_name="Имя", max_length=50)
    last_name = models.CharField(verbose_name="Фамилия", max_length=50)
    registered_at = models.DateField(verbose_name="Дата регистрации", auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="Email", null=True)

    class Meta:
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self) -> str:
        return reverse("update_profile", kwargs={"slug": self.created_by.pk})


class Category(models.Model):
    """
    Класс, описывающий категорию объектов недвижимости
    :param name: Название категории
    :param slug: Репрезентация части url адреса для категории
                 (заполняется автоматически при создании)
    """

    name = models.CharField(verbose_name='Название', max_length=100, unique=True)
    slug = models.SlugField(verbose_name='Ссылка', max_length=100, unique=True, editable=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.slug = translit.slugify(f"category-{self.name}")
        super(Category, self).save(*args, **kwargs)


class Tag(models.Model):
    """
    Класс, описывающий тэг объектов недвижимости
    :param name: Название категории
    :param slug: Репрезентация части url адреса для категории
                 (заполняется автоматически при создании)
    :param realty_list: Список привязанных к тэгу объектов недвижимости
    """
    name = models.CharField(verbose_name='Название', max_length=100, unique=True)
    slug = models.SlugField(verbose_name='Ссылка', max_length=100, unique=True, editable=False)
    realty_list = models.ManyToManyField(Realty, related_name="realty_list")

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.slug = translit.slugify(f"tag-{self.name}")
        super(Tag, self).save(*args, **kwargs)


class Subscriber(models.Model):
    """
    Класс, описывающий модель подписчика - связан с пользователем сайта
    :param user: объект пользователя (User), который создал профиль
    :param novelty_subscribed: Подписан ли пользователь на новинки
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    novelty_subscribed = models.BooleanField(verbose_name="Подписка на новинки", default=False)

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self) -> str:
        return self.user.username
