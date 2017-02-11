from uuid import uuid4

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db.models import Model, CharField, TextField, FileField, ImageField, BooleanField, ForeignKey, \
    DateTimeField, IntegerField, DecimalField, SlugField, PositiveSmallIntegerField, UUIDField, URLField, Sum
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField
from moneyed import Money


class User(AbstractUser):
    interest_in_site = ForeignKey('UserInterestInSite', related_name='users', blank=True, null=True)
    verified = BooleanField(default=False)

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


class Country(Model):
    name = CharField(max_length=255)
    iso_alpha_2 = CharField(max_length=2)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class City(Model):
    name = CharField(max_length=255)
    country = ForeignKey('Country', related_name='cities')
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255)
    city = ForeignKey('City', related_name='districts')
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Project(Model):
    title = CharField(max_length=255)
    slug = SlugField()
    description = TextField()
    cover_image = ForeignKey('ProjectImage', related_name='covered_project')
    video = FileField(upload_to='uploads/videos/', null=True, blank=True)
    matterport_url = URLField(blank=True, null=True)
    is_allowed_on_home_page = BooleanField(default=False)
    goal = MoneyField(max_digits=12, decimal_places=2, default_currency='SGD')
    minimal_investment_amount = MoneyField(max_digits=12, decimal_places=2, default_currency='SGD')
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
    country = ForeignKey('Country', related_name='projects', null=True, blank=True)
    city = ForeignKey('City', related_name='projects', null=True, blank=True)
    district = ForeignKey('District', related_name='districts', null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_detail_slug', args=[str(self.id), self.slug])

    # FIXME: WHY DOES THIS NET DUPLICATE QUERIES?
    @property
    def currently_invested_total_sum(self):
        if not hasattr(self, 'currently_invested_total_sum_cache'):
            try:
                self.currently_invested_total_sum_cache = [Money(data['value__sum'], data['value_currency']) for data in
                      self.investments.values('value_currency').annotate(Sum('value')).order_by()][0]
            except IndexError:
                self.currently_invested_total_sum_cache = 0

        return self.currently_invested_total_sum_cache


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
    DEPOSIT, WITHDRAWAL, INVESTMENT = range(3)
    TRANSACTION_TYPE_CHOICES = (
        (DEPOSIT, _('Deposit')),
        (WITHDRAWAL, _('Withdrawal')),
        (INVESTMENT, _('Investment')),
    )
    user = ForeignKey('User', related_name='transactions')
    type = PositiveSmallIntegerField(choices=TRANSACTION_TYPE_CHOICES)
    investment = ForeignKey('Investment', related_name='transactions', null=True, blank=True)
    amount = MoneyField(max_digits=12, decimal_places=2, default_currency='SGD')
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return ' - '.join([self.user.username, self.get_type_display(), str(self.amount)])


class Investment(Model):
    token = UUIDField(default=uuid4, editable=False)
    project = ForeignKey('Project', related_name='investments')
    user = ForeignKey('User', related_name='investments')
    value = MoneyField(max_digits=12, decimal_places=2, default_currency='SGD')
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return ' - '.join([str(self.token), self.project.title, self.user.username])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            send_mail(
                'User invested on Unreal Estate demo site',
                'User ID: %d, project ID: %d' % (self.user.pk, self.project.pk),
                settings.DEFAULT_FROM_EMAIL,
                [x[1] for x in settings.ADMINS]
            )
        super(Investment, self).save(force_insert, force_update, using, update_fields)


class ProjectProposal(Model):
    user = ForeignKey('User', related_name='project_proposals')
    name = CharField(max_length=255)
    location = CharField(max_length=255)
    preferred_price = MoneyField(max_digits=12, decimal_places=2, default_currency='SGD')
    short_description = TextField()
    type = ForeignKey('AssetClass', related_name='project_proposals')
    size = CharField(max_length=255)
    tenancy = BooleanField(default=False)
    tenancy_agreement_length = CharField(max_length=255)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectProposalImage(Model):
    project_proposal = ForeignKey('ProjectProposal', related_name='pictures')
    image = ImageField(upload_to='uploads/images/')
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.image.name


class FAQ(Model):
    question = CharField(max_length=255)
    answer = TextField()
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.question