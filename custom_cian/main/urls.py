from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('realty_list/', views.RealtyListView.as_view(), name="realty_list"),
    path('realty_list/<slug:slug>/', views.RealtyDetailView.as_view(), name="realty_detail"),
    path('realty_list/<slug:slug>/edit', views.RealtyUpdateView.as_view(), name="update_realty"),
    path('accounts/profile/<int:pk>/', views.SallerUpdateView.as_view(), name="update_profile"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='main/login.html'), name="login"),
    path('realty/add/', views.RealtyCreateView.as_view(), name="add_realty")
]
