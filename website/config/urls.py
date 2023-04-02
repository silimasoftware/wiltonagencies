from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from wiltonagencies.views import (
    page_loader_view,
)
from django.contrib.sitemaps.views import sitemap
from .sitemap import Home, About, Contact

handler404 = "wiltonagencies.views.page_not_found_view"

sitemaps = {"wiltonagencies": Home, "about": About, "contact": Contact}

urlpatterns = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", page_loader_view, name="wiltonagencies"),
    path("<slug:page>/", page_loader_view, name="wiltonagencies"),
    path("<slug:page>/<slug:function>/", page_loader_view, name="wiltonagencies"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
