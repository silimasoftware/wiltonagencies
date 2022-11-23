from django.contrib import sitemaps
from django.urls import reverse


class Home(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return ["wiltonagencies"]

    def location(self, obj):
        return ""


class About(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return ["about"]

    def location(self, obj):
        return "about/"


class Contact(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return ["contact"]

    def location(self, obj):
        return "contact/"
