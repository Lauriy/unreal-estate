from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Model, CharField, TextField, FileField, ImageField, BooleanField, ForeignKey, \
    DateTimeField, IntegerField, DecimalField, OneToOneField
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User


class AssetClass(Model):
    name = CharField(max_length=255)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class InvestmentType(Model):
    name = CharField(max_length=255)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Project(Model):
    title = CharField(max_length=255)
    description = TextField()
    video = FileField(upload_to='uploads/videos/', null=True, blank=True)
    is_allowed_on_home_page = BooleanField(default=False)
    goal = MoneyField(max_digits=12, decimal_places=2, default_currency='SGD')
    deadline = DateTimeField()
    asset_class = ForeignKey('AssetClass', related_name='projects')
    investment_type = ForeignKey('InvestmentType', related_name='projects')
    investment_period_months = IntegerField()
    expected_rate_of_return = DecimalField(max_digits=4, decimal_places=2)
    analysis_general = RichTextUploadingField()
    analysis_location = RichTextUploadingField()
    analysis_market = RichTextUploadingField()
    analysis_project = RichTextUploadingField()
    analysis_financial = RichTextUploadingField()
    analysis_documents = RichTextUploadingField()
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProjectImage(Model):
    project = ForeignKey('Project', related_name='images')
    image = ImageField(upload_to='uploads/images/')
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.image.name


# class Profile(Model):
#     user = OneToOneField(User)
#
#     def __str__(self):
#         return self.user.username