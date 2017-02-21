from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from unrealestate.models import Project


class ProjectSitemap(Sitemap):
    priority = 1

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.modified


class StaticViewSitemap(Sitemap):
    priority = 1

    def items(self):
        return ['home', 'offerings', 'about_us', 'faq']

    def location(self, item):
        return reverse(item)
