from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from unrealestate.models import AssetClass, InvestmentType, Project, ProjectImage, UserInterestInSite, User


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(User, UserAdmin)
admin.site.register(UserInterestInSite)
admin.site.register(AssetClass)
admin.site.register(InvestmentType)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectImage)
