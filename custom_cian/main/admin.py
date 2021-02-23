from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from django.db import models

from ckeditor.widgets import CKEditorWidget

from .models import Category, Saller, Realty, Tag, Subscriber


class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Category)

# временно зарегистрированы для удобства добавления
admin.site.register(Realty)
admin.site.register(Saller)
admin.site.register(Tag)
admin.site.register(Subscriber)
