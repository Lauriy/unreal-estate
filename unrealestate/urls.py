from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from unrealestate.views import HomeView, AboutUsView, SignUpView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^comments/', include('django_comments_xtd.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^$', HomeView.as_view(), name='home'),
    url(_(r'^about-us/$'), AboutUsView.as_view(), name='about_us'),
    url(_(r'^sign-up/$'), SignUpView.as_view(), name='sign_up'),
)
