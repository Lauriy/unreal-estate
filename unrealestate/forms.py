from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField, Textarea, ModelChoiceField, TextInput, DateField, ChoiceField, \
    FileField
from django.utils.translation import ugettext_lazy as _
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField
from djmoney.forms import MoneyField
from haystack.forms import SearchForm
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES
from localflavor.generic.forms import IBANFormField, BICFormField
from phonenumber_field.formfields import PhoneNumberField

from unrealestate.models import Project, InvestmentType, Country, City, District, UserInterestInSite


class SignupForm(Form):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    interest = ModelChoiceField(queryset=UserInterestInSite.objects.all())

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.interest_in_site = self.cleaned_data['interest']
        user.save()


class AddFundsForm(Form):
    amount = MoneyField(max_digits=12, decimal_places=2, min_value=0.01)


class WithdrawFundsForm(Form):
    amount = MoneyField(max_digits=12, decimal_places=2, min_value=0.01)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WithdrawFundsForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if self.user.get_account_balance() < data:
            raise ValidationError(_('Insufficient funds'))

        return data


class FAQForm(Form):
    contact_name = CharField(max_length=255)
    contact_email = EmailField()
    question = CharField(widget=Textarea)


class InvestmentForm(Form):
    amount = MoneyField(max_digits=12, decimal_places=2, min_value=0.01)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.project = kwargs.pop('project', None)
        super(InvestmentForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if self.user.get_account_balance() < data:
            raise ValidationError(_('Insufficient funds'))
        if self.project.goal - self.project.get_currently_invested_total_sum() < data:
            raise ValidationError(_('Investment too large, %s left to goal completion'))

        return data


class HaystackProjectSearchForm(SearchForm):
    type = ModelChoiceField(queryset=InvestmentType.objects.all(), required=False)
    country = ModelChoiceField(queryset=Country.objects.all(), required=False)
    city = ModelChoiceField(queryset=City.objects.all(), required=False)
    district = ModelChoiceField(queryset=District.objects.all(), required=False)
    date_added_from = DateField(required=False)
    date_added_until = DateField(required=False)
    goal_from = MoneyField(max_digits=12, decimal_places=2, min_value=0.01, required=False)
    goal_up_to = MoneyField(max_digits=12, decimal_places=2, min_value=0.01, required=False)

    def __init__(self, *args, **kwargs):
        super(HaystackProjectSearchForm, self).__init__(*args, **kwargs)
        self.fields['q'].widget = TextInput(attrs={'type': 'text'})
        self.fields['date_added_from'].widget = TextInput(attrs={'type': 'date'})
        self.fields['date_added_until'].widget = TextInput(attrs={'type': 'date'})

    def search(self):
        sqs = super(HaystackProjectSearchForm, self).search().models(Project)

        if not self.is_valid():
            return self.no_query_found()

        return sqs


class VerificationForm(Form):
    FEMALE, MALE = range(2)
    GENDER_CHOICES = (
        (FEMALE, _('Female')),
        (MALE, _('Male'))
    )
    PASSPORT, ID_CARD, DRIVING_LICENCE = range(3)
    DOCUMENT_CHOICES = (
        (PASSPORT, _('Passport')),
        (ID_CARD, _('ID-card')),
        (DRIVING_LICENCE, _('Driving licence'))
    )
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    email = EmailField()
    date_of_birth = DateField()
    nationality = LazyTypedChoiceField(choices=countries)
    address_line_1 = CharField(max_length=50)
    address_line_2 = CharField(max_length=50)
    gender = ChoiceField(choices=GENDER_CHOICES)
    phone_number = PhoneNumberField()
    iban_owner = CharField(max_length=60)
    iban = IBANFormField(include_countries=IBAN_SEPA_COUNTRIES)
    bic = BICFormField()
    bank_statement = FileField()
    document_type = ChoiceField(choices=DOCUMENT_CHOICES)
    document = FileField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(VerificationForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = TextInput(attrs={'type': 'date'})
        self.initial['first_name'] = self.user.first_name
        self.initial['last_name'] = self.user.last_name
        self.initial['email'] = self.user.email