from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from unrealestate.models import User, Project


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


class ProfileView(UpdateView, LoginRequiredMixin):
    template_name = 'profile.html'
    model = User
    fields = ['first_name', 'last_name', 'interest_in_site']

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('account_profile')


class ProjectDetailView(DetailView):
    model = Project
