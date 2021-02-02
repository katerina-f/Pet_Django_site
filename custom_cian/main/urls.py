from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('realty_list/', views.RealtyListView.as_view(), name="realty_list"),
    path('realty_list/<slug:slug>/', views.RealtyDetailView.as_view(), name="realty_detail"),
    path('realty_list/<slug:slug>/edit', views.RealtyUpdateView.as_view(), name="update_realty"),
    path('accounts/profile/<int:pk>/', views.SallerUpdateView.as_view(), name="update_profile"),
    path('realty/add/', views.RealtyCreateView.as_view(), name="add_realty"),
    path('registration/', views.registration, name="registration"),
    path('accounts/', include('django.contrib.auth.urls')),
]
