from django.db import models


class Nav(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = "core"

    def __str__(self):
        return self.name


class Link(models.Model):
    nav = models.ForeignKey(Nav, related_name="link", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=255, default="", blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        app_label = "core"
        ordering = ("order",)

    def __str__(self):
        return self.name
