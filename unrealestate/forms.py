from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField, Textarea, ModelChoiceField, TextInput, DateField
from django.utils.translation import ugettext_lazy as _
from djmoney.forms import MoneyField
from haystack.forms import SearchForm

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
