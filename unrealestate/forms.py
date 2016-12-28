from django.core.exceptions import ValidationError
from django.forms import Form
from django.utils.translation import ugettext_lazy as _
from djmoney.forms import MoneyField


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
