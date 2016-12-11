from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from unrealestate.views import HomeView, AboutUsView, SignUpView, ProfileView, ProjectDetailView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', ProfileView.as_view(), name='account_profile'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^comments/', include('django_comments_xtd.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^$', HomeView.as_view(), name='home'),
    url(_(r'^about-us/$'), AboutUsView.as_view(), name='about_us'),
    url(_(r'^sign-up/$'), SignUpView.as_view(), name='sign_up'),
    url(_(r'^projects/(?P<id>\d+)/$'), ProjectDetailView.as_view(), name='project_detail_id'),
    url(_(r'^projects/(?P<id>\d+)/(?P<slug>[-\w]+)/$'), ProjectDetailView.as_view(), name='project_detail_slug'),
)