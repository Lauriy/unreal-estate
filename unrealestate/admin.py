from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from unrealestate.models import AssetClass, InvestmentType, Project, ProjectImage, UserInterestInSite, User, Investment, \
    Transaction, Country, City, District, ProjectProposal, ProjectProposalImage, FAQ


class MyUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff', 'interest_in_site',
                    'verified')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('verified', 'interest_in_site')}),
    )


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    fields = ('image',)


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ProjectImageInline,)


class ProjectProposalImageInline(admin.TabularInline):
    model = ProjectProposalImage
    fields = ('image',)


class ProjectProposalAdmin(admin.ModelAdmin):
    model = ProjectProposal
    inlines = (ProjectProposalImageInline,)


admin.site.register(User, MyUserAdmin)
admin.site.register(UserInterestInSite)
admin.site.register(AssetClass)
admin.site.register(InvestmentType)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectImage)
admin.site.register(Investment)
admin.site.register(Transaction)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(District)
admin.site.register(ProjectProposal, ProjectProposalAdmin)
admin.site.register(ProjectProposalImage)
admin.site.register(FAQ)
