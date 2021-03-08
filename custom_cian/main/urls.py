from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from rest_framework import routers

from . import views
from .sitemap import RealtySitemap, StaticPagesSitemap


sitemaps = {
    "realty_objects": RealtySitemap,
    "static": StaticPagesSitemap
}


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'realty_list', views.RealtyViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'sallers', views.SallerViewSet)


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
         name='django.contrib.sitemaps.views.sitemap'),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt",
                             content_type="text/plain"),
    ),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
