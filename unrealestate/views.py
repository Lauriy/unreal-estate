from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from unrealestate.forms import AddFundsForm, WithdrawFundsForm
from unrealestate.models import User, Project, Transaction, Investment


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['sample_projects'] = Project.objects.filter(is_allowed_on_home_page=True)[
                                     :settings.SAMPLE_PROJECTS_ON_HOME_PAGE]

        return context


class AboutUsView(TemplateView):
    template_name = 'about_us.html'


class SignUpView(TemplateView):
    template_name = 'sign_up.html'


class ProfileEditView(UpdateView, LoginRequiredMixin):
    template_name = 'profile_edit.html'
    model = User
    fields = ['first_name', 'last_name', 'interest_in_site']

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('account_profile')


class ProfileAddFundsView(FormView, LoginRequiredMixin):
    template_name = 'profile_add_funds.html'
    form_class = AddFundsForm

    def form_valid(self, form):
        Transaction(
            user=self.request.user,
            type=Transaction.DEPOSIT,
            amount=form.cleaned_data['amount']
        ).save()
        return super(ProfileAddFundsView, self).form_valid(form)

    def get_success_url(self):
        return reverse('account_fake_bank')


class ProfileWithdrawFundsView(FormView, LoginRequiredMixin):
    template_name = 'profile_withdraw_funds.html'
    form_class = WithdrawFundsForm

    def get_form_kwargs(self):
        kwargs = super(ProfileWithdrawFundsView, self).get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def get_success_url(self):
        return reverse('account_fake_bank')

    def form_valid(self, form):
        Transaction(
            user=self.request.user,
            type=Transaction.WITHDRAWAL,
            amount=form.cleaned_data['amount']
        ).save()
        return super(ProfileWithdrawFundsView, self).form_valid(form)


class ProjectDetailView(DetailView):
    model = Project


class FakeBankView(TemplateView):
    template_name = 'fake_bank.html'


class ProfileTransactionsView(ListView, LoginRequiredMixin):
    model = Transaction
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.transactions.all()

    def get_context_data(self, **kwargs):
        context = super(ProfileTransactionsView, self).get_context_data(**kwargs)
        context['account_balance'] = self.request.user.get_account_balance()

        return context


class ProfileInvestmentsView(ListView, LoginRequiredMixin):
    model = Investment
