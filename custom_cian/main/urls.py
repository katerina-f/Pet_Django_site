from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('realty_list/', views.RealtyListView.as_view(), name="realty_list"),
    path('realty_list/<slug:slug>/', views.RealtyDetailView.as_view(), name="realty_detail"),
    path('realty_list/<slug:slug>/edit', views.RealtyUpdateView.as_view(), name="update_realty"),
    path('accounts/profile/<slug:slug>/', views.SallerUpdateView.as_view(), name="update_profile"),
    path('realty/add/', views.RealtyCreateView.as_view(), name="add_realty"),
    path('accounts/', include('allauth.urls')),
]
