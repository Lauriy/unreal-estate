from django.contrib import admin

from unrealestate.models import AssetClass, InvestmentType, Project, ProjectImage

admin.site.register(AssetClass)
admin.site.register(InvestmentType)
admin.site.register(Project)
admin.site.register(ProjectImage)
