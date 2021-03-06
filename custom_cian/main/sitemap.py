from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Realty


class RealtySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Realty.objects.all()


class StaticPagesSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'about', 'contacts']

    def location(self, item):
        return reverse(item)
