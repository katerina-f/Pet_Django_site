from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework import permissions

from .models import Realty, Saller, Category
from .serializers import UserSerializer, \
                         GroupSerializer, \
                         RealtySerializer, \
                         CategorySerializer, \
                         SallerSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class RealtyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows realty objects to be viewed or edited.
    """
    queryset = Realty.objects.all()
    serializer_class = RealtySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class SallerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sallers to be viewed or edited.
    """
    queryset = Saller.objects.all()
    serializer_class = SallerSerializer
    permission_classes = [permissions.IsAuthenticated]
