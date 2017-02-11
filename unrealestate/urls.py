from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _

from unrealestate.views import HomeView, AboutUsView, FAQView, ProfileEditView, ProjectDetailView, \
    ProfileAddFundsView, ProfileWithdrawFundsView, ProfileTransactionsView, ProfileInvestmentsView, FakeBankView, \
    OfferingsView, SellYourPropertyView, ProfileVerificationView, FakeVerificationView, LearnMoreEmailTriggerView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home_no_locale'),
    url(r'^admin/', admin.site.urls),
    url(r'^drf-projects/(?P<pk>[0-9]+)/$', LearnMoreEmailTriggerView.as_view(), name='drf-retrieve-project'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', ProfileEditView.as_view(), name='account_profile'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^comments/', include('django_comments_xtd.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    # from django.conf.urls.static import static

    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += i18n_patterns(
    url(r'^$', HomeView.as_view(), name='home'),
    url(_(r'^offerings/$'), OfferingsView.as_view(), name='offerings'),
    url(_(r'^sell-your-property/$'), SellYourPropertyView.as_view(), name='sell_your_property'),
    url(_(r'^about-us/$'), AboutUsView.as_view(), name='about_us'),
    url(_(r'^faq/$'), FAQView.as_view(), name='faq'),
    url(_(r'^project/(?P<id>\d+)/$'), ProjectDetailView.as_view(), name='project_detail_id'),
    url(_(r'^project/(?P<id>\d+)/(?P<slug>[-\w]+)/$'), ProjectDetailView.as_view(), name='project_detail_slug'),
    url(_(r'^accounts/add-funds/$'), ProfileAddFundsView.as_view(), name='account_add_funds'),
    url(_(r'^accounts/transactions/$'), ProfileTransactionsView.as_view(), name='account_transactions'),
    url(_(r'^accounts/transactions/fake-bank/$'), FakeBankView.as_view(), name='account_fake_bank'),
    url(_(r'^accounts/withdraw-funds/$'), ProfileWithdrawFundsView.as_view(), name='account_withdraw_funds'),
    url(_(r'^accounts/investments/$'), ProfileInvestmentsView.as_view(), name='account_investments'),
    url(_(r'^accounts/verify/$'), ProfileVerificationView.as_view(), name='account_verify'),
    url(_(r'^accounts/verify/fake/$'), FakeVerificationView.as_view(), name='account_fake_verify'),
)
