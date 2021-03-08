from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Realty, Category, Saller


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class RealtySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Realty
        exclude = ['counter']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SallerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Saller
        fields = '__all__'
