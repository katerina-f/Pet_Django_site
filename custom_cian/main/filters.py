import django_filters

from .models import Realty


class RealtyFilter(django_filters.FilterSet):

    class Meta:
        model = Realty
        fields = {
            'price': ['lt', 'gt'],
            'published_at': ['exact', 'year__gt'],
            'category__name': ['icontains'],
            'saller__last_name': ['icontains'],
        }
