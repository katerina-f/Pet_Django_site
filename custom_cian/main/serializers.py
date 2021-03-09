import re

from django.contrib.auth.models import User, Group
from rest_framework import serializers, fields

from .models import Realty, Category, Saller


class StringArrayField(fields.ListField):
    """
    Кастомное поле для сериализации списка строк как строки и обратно
    """
    def to_representation(self, obj):
        obj = super().to_representation(obj)
        # convert list to string
        return ",".join([str(element) for element in obj])

    def to_internal_value(self, data):
        data = data.split(",")  # convert string to list
        return super().to_internal_value(self, data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class RealtySerializer(serializers.HyperlinkedModelSerializer):
    tags = fields.CharField(style={'base_template': 'textarea.html'})

    class Meta:
        model = Realty
        fields = '__all__'
        read_only_fields = ['counter', 'slug']

    def to_representation(self, ret):
        ret = super().to_representation(ret)
        # convert list to string
        ret["tags"] = re.sub("[\[\]']", "", ret["tags"])
        ret["tags"] = ",".join(ret["tags"].split(","))
        return ret

    def to_internal_value(self, ret):
        ret = super().to_internal_value(ret)
        ret["tags"] = ret["tags"].split(",")  # convert string to list
        return ret


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SallerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Saller
        fields = '__all__'
