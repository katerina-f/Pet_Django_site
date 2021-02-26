from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from django.db import models
from django.utils.translation import ngettext

from ckeditor.widgets import CKEditorWidget

from .models import Category, Saller, Realty, Tag, Subscriber


class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


class RealtyAdmin(admin.ModelAdmin):
    ordering = ("-published_at", "tags")
    actions = ["create_multiple_realty",]

    def create_multiple_realty(self, request):
        print(request)

    create_multiple_realty.short_description = ngettext("Bulk create realty", "Bulk create realty", 1.0)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Category)
admin.site.register(Realty, RealtyAdmin)

# временно зарегистрированы для удобства добавления

admin.site.register(Saller)
admin.site.register(Tag)
admin.site.register(Subscriber)
