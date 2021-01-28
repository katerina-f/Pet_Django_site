from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('realty_list/', views.RealtyListView.as_view(), name="realty_list"),
    path('realty_list/<slug:slug>/', views.RealtyDetailView.as_view(), name="realty_detail")
]
