from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

from . import views, sitemaps


sitemaps = {
    "realty_objects": sitemaps.RealtySitemap,
    "static": sitemaps.StaticPagesSitemap
}


urlpatterns = [
    path('', views.index, name="index"),
    path('realty_list/', views.RealtyListView.as_view(), name="realty_list"),
    path('user_realty_list/', views.UserRealtyView.as_view(), name="user_realty_list"),
    path('realty_list/<slug:slug>/', views.RealtyDetailView.as_view(), name="realty_detail"),
    path('realty_list/<slug:slug>/edit', views.RealtyUpdateView.as_view(), name="update_realty"),
    path('accounts/profile/<slug:slug>/', views.SallerUpdateView.as_view(), name="update_profile"),
    path('realty/add/', views.RealtyCreateView.as_view(), name="add_realty"),
    path('accounts/', include('allauth.urls')),
    path('subscribe/', views.subscribe_on_novelty, name="subscribe"),
    path('search/', views.SearchListView.as_view(), name="search"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]
