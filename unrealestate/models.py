from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, TextField, FileField, ImageField, BooleanField, ForeignKey, \
    DateTimeField, IntegerField, DecimalField, SlugField, PositiveSmallIntegerField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField


class User(AbstractUser):
    interest_in_site = ForeignKey('UserInterestInSite', related_name='users', blank=True, null=True)

    # TODO: In the future, cache this
    def get_account_balance(self):
        balance = 0
        for transaction in self.transactions.all():
            if transaction.type == Transaction.DEPOSIT:
                balance += transaction.amount
            else:
                balance -= transaction.amount

        return balance


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
    slug = SlugField()
    description = TextField()
    video = FileField(upload_to='uploads/videos/', null=True, blank=True)
    is_allowed_on_home_page = BooleanField(default=False)
    goal = MoneyField(max_digits=12, decimal_places=2, default_currency='SGD')
    deadline = DateTimeField()
    asset_class = ForeignKey('AssetClass', related_name='projects')
    investment_type = ForeignKey('InvestmentType', related_name='projects')
    investment_period_months = IntegerField()
    expected_rate_of_return = DecimalField(max_digits=4, decimal_places=2)
    analysis_general_intro = CharField(max_length=255, null=True, blank=True)
    analysis_general = RichTextUploadingField(null=True, blank=True)
    analysis_location_intro = CharField(max_length=255, null=True, blank=True)
    analysis_location = RichTextUploadingField(null=True, blank=True)
    analysis_market_intro = CharField(max_length=255, null=True, blank=True)
    analysis_market = RichTextUploadingField(null=True, blank=True)
    analysis_project_intro = CharField(max_length=255, null=True, blank=True)
    analysis_project = RichTextUploadingField(null=True, blank=True)
    analysis_financial_intro = CharField(max_length=255, null=True, blank=True)
    analysis_financial = RichTextUploadingField(null=True, blank=True)
    analysis_documents_intro = CharField(max_length=255, null=True, blank=True)
    analysis_documents = RichTextUploadingField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_detail_slug', args=[str(self.id), self.slug])


class ProjectImage(Model):
    project = ForeignKey('Project', related_name='images')
    image = ImageField(upload_to='uploads/images/')
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.image.name


class UserInterestInSite(Model):
    name = CharField(max_length=255)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Transaction(Model):
    DEPOSIT, WITHDRAWAL = range(2)
    TRANSACTION_TYPE_CHOICES = (
        (DEPOSIT, _('Deposit')),
        (WITHDRAWAL, _('Withdrawal')),
    )
    user = ForeignKey('User', related_name='transactions')
    type = PositiveSmallIntegerField(choices=TRANSACTION_TYPE_CHOICES)
    amount = MoneyField(max_digits=12, decimal_places=2, default_currency='SGD')
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)


class Investment(Model):
    pass
