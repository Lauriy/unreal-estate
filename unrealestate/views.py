from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Sum, Count
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from unrealestate.forms import AddFundsForm, WithdrawFundsForm, FAQForm, InvestmentForm, HaystackProjectSearchForm, \
    VerificationForm
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


class FAQView(FormView):
    template_name = 'faq.html'
    form_class = FAQForm

    def get_success_url(self):
        return reverse('faq')

    def get_form_kwargs(self):
        kwargs = super(FAQView, self).get_form_kwargs()
        if self.request.method == 'POST' and self.request.user.is_authenticated():
            self.request.POST._mutable = True
            self.request.POST['contact_name'] = self.request.user.first_name + ' ' + self.request.user.last_name
            self.request.POST['contact_email'] = self.request.user.email

        return kwargs

    def form_valid(self, form):
        send_mail(
            'Unreal Estate FAQ question',
            form.cleaned_data['contact_name'] + ': ' + form.cleaned_data['question'],
            form.cleaned_data['contact_email'],
            ['team@unrealestate.sg'],
            fail_silently=False,
        )

        return super(FAQView, self).form_valid(form)


class SignUpView(TemplateView):
    template_name = 'sign_up.html'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'profile_edit.html'
    model = User
    fields = ['first_name', 'last_name', 'interest_in_site']

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('account_profile')


class ProfileAddFundsView(UserPassesTestMixin, FormView):
    template_name = 'profile_add_funds.html'
    form_class = AddFundsForm
    login_url = 'account_verify'

    def form_valid(self, form):
        Transaction(
            user=self.request.user,
            type=Transaction.DEPOSIT,
            amount=form.cleaned_data['amount']
        ).save()
        return super(ProfileAddFundsView, self).form_valid(form)

    def get_success_url(self):
        return reverse('account_fake_bank')

    def test_func(self):
        return self.request.user.is_authenticated() and self.request.user.verified


class ProfileWithdrawFundsView(UserPassesTestMixin, FormView):
    template_name = 'profile_withdraw_funds.html'
    form_class = WithdrawFundsForm
    login_url = 'account_verify'

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

    def test_func(self):
        return self.request.user.is_authenticated() and self.request.user.verified


def user_is_verified_test(user):
    return user.verified


investment_decorators = [login_required, user_passes_test(user_is_verified_test)]


class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        form = InvestmentForm()
        context['form'] = form

        return context

    # Don't remove unused args, kwargs
    @method_decorator(investment_decorators)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = InvestmentForm(request.POST, user=request.user, project=self.object)
        if form.is_valid():
            Investment(
                user=request.user,
                project=self.object,
                value=form.cleaned_data['amount']
            ).save()
            Transaction(
                user=request.user,
                type=Transaction.INVESTMENT,
                amount=form.cleaned_data['amount']
            ).save()

        context = self.get_context_data()
        context['form'] = form

        return super(ProjectDetailView, self).render_to_response(context)


class FakeBankView(TemplateView):
    template_name = 'fake_bank.html'


class FakeVerificationView(TemplateView):
    template_name = 'fake_verification.html'


class ProfileTransactionsView(UserPassesTestMixin, ListView):
    model = Transaction
    paginate_by = 10
    login_url = 'account_verify'

    def get_queryset(self):
        return self.request.user.transactions.all()

    def get_context_data(self, **kwargs):
        context = super(ProfileTransactionsView, self).get_context_data(**kwargs)
        context['account_balance'] = self.request.user.get_account_balance()

        return context

    def test_func(self):
        return self.request.user.is_authenticated() and self.request.user.verified


class ProfileInvestmentsView(UserPassesTestMixin, ListView):
    model = Investment
    paginate_by = 10
    login_url = 'account_verify'

    def get_queryset(self):
        return self.request.user.investments.all()

    def test_func(self):
        return self.request.user.is_authenticated() and self.request.user.verified


class OfferingsView(ListView):
    model = Project
    paginate_by = 12

    def get_queryset(self):
        qs = super(OfferingsView, self).get_queryset()
        search_form = HaystackProjectSearchForm(self.request.GET)
        if search_form.is_valid():
            if search_form.cleaned_data['type']:
                qs = qs.filter(investment_type=search_form.cleaned_data['type'])
            if search_form.cleaned_data['country']:
                qs = qs.filter(country=search_form.cleaned_data['country'])
            if search_form.cleaned_data['city']:
                qs = qs.filter(city=search_form.cleaned_data['city'])
            if search_form.cleaned_data['district']:
                qs = qs.filter(district=search_form.cleaned_data['district'])
            if search_form.cleaned_data['date_added_from']:
                qs = qs.filter(created__gte=search_form.cleaned_data['date_added_from'])
            if search_form.cleaned_data['date_added_until']:
                qs = qs.filter(created__lte=search_form.cleaned_data['date_added_until'])
            if search_form.cleaned_data['goal_from']:
                qs = qs.filter(goal__gte=search_form.cleaned_data['goal_from'])
            if search_form.cleaned_data['goal_up_to']:
                qs = qs.filter(goal__lte=search_form.cleaned_data['goal_up_to'])
            if search_form.cleaned_data['q']:
                search_query_set = search_form.search()
                results = [r.pk for r in search_query_set]
                qs = qs.filter(pk__in=results)
        qs = qs.annotate(invested_sum=Sum('investments__value'))
        qs = qs.annotate(investors=Count('investments__user', distinct=True))

        return qs

    def get_context_data(self, **kwargs):
        context = super(OfferingsView, self).get_context_data(**kwargs)
        search_form = HaystackProjectSearchForm(self.request.GET)
        search_form.is_valid()
        context['form'] = search_form

        return context


class SellYourPropertyView(UserPassesTestMixin, TemplateView):
    template_name = 'sell_your_property.html'
    login_url = 'account_verify'

    def test_func(self):
        return self.request.user.is_authenticated() and self.request.user.verified


class ProfileVerificationView(LoginRequiredMixin, FormView):
    template_name = 'profile_verify.html'
    form_class = VerificationForm

    def get_form_kwargs(self):
        kwargs = super(ProfileVerificationView, self).get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def get_success_url(self):
        return reverse('account_fake_verify')

    def form_valid(self, form):
        self.request.user.verified = True
        self.request.user.save()
        return super(ProfileVerificationView, self).form_valid(form)