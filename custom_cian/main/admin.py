from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib import messages
from django.db import models
from django.utils.translation import ngettext

from ckeditor.widgets import CKEditorWidget
from pytils import numeral

from .models import Category, Saller, Realty, Tag, Subscriber


class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


class RealtyAdmin(admin.ModelAdmin):
    ordering = ("-published_at", "tags")
    actions = ["push_to_archive",]

    def push_to_archive(self, request, queryset):
        updated = queryset.update(in_archive=True)
        obj = numeral.sum_string(updated, numeral.MALE, (u"объект", u"объекта", u"объектов"))
        self.message_user(request, ngettext(
            '%s успешно отправлен в архив',
            '%s успешно отправлены в архив',
            updated,
        ) % obj, messages.SUCCESS)

    push_to_archive.short_description = "Отправить выбранные объекты в архив"


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Category)
admin.site.register(Realty, RealtyAdmin)

# временно зарегистрированы для удобства добавления

admin.site.register(Saller)
admin.site.register(Tag)
admin.site.register(Subscriber)
