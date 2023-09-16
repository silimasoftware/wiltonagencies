from django.contrib import admin
from .models import Nav, Link


@admin.register(Nav)
class NavAdmin(admin.ModelAdmin):
    pass


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "link",
        "nav",
        "order",
    )


