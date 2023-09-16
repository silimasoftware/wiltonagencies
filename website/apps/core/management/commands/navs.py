from django.core.management.base import BaseCommand
from core.models import Link, Nav
from core.util import get_object_or_404


class Command(BaseCommand):
    def handle(self, *args, **options):
        Link.objects.all().delete()
        Nav.objects.all().delete()

        # create portal nav
        portal_nav = Nav(name="portal")
        portal_nav.save()
        n = 0
        
        portal_links = {
            "Leads": "leads",
            "Clients": "clients",
            "Products": "products",
        }
        for k in portal_links:
            page_nav = Nav(name=portal_links[k].lower())
            page_nav.save()
            link = Link(name=k, nav=portal_nav, link=portal_links[k].lower(), order=n)
            link.save()
            n += 1
