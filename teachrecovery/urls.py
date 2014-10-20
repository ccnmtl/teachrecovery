import os.path

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from teachrecovery.main import views
from teachrecovery.main.views import TeachRecoveryPageView, \
    TeachRecoveryEditView


admin.autodiscover()


site_media_root = os.path.join(os.path.dirname(__file__), "../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (
    r'^accounts/logout/$',
    'django.contrib.auth.views.logout',
    {'next_page': redirect_after_logout})

admin_logout_page = (r'^accounts/logout/$',
                     'django.contrib.auth.views.logout',
                     {'next_page': '/admin/'})

if hasattr(settings, 'CAS_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (
        r'^accounts/logout/$',
        'djangowind.views.logout',
        {'next_page': redirect_after_logout})
    admin_logout_page = (r'^admin/logout/$',
                         'djangowind.views.logout',
                         {'next_page': redirect_after_logout})

urlpatterns = patterns(
    '',
    logout_page,
    admin_logout_page,
    auth_urls,
    
    (r'^registration/', include('registration.backends.default.urls')),
    url(r'^$', views.index, name="index"),
    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^quizblock/', include('quizblock.urls')),
    (r'^quizblock_random/', include('quizblock_random.urls')),

    (r'^pages_save_edit/(?P<hierarchy_name>[-\w]+)/(?P<path>.*)$',
        'teachrecovery.main.views.pages_save_edit'),

    # (r'^pages/edit/(?P<path>.*)$', EditPage.as_view(),
    #  {}, 'edit-page'),
    # (r'^pages/instructor/(?P<path>.*)$',
    #  'teachrecovery.main.views.instructor_page'),
    # (r'^pages/(?P<path>.*)$', ViewPage.as_view()),

    (r'^pages/(?P<hierarchy_name>[-\w]+)/edit/(?P<path>.*)$',
     TeachRecoveryEditView.as_view()),
    (r'^pages/(?P<hierarchy_name>[-\w]+)/instructor/(?P<path>.*)$',
     'teachrecovery.main.views.instructor_page'),
    (r'^pages/(?P<hierarchy_name>[-\w]+)/(?P<path>.*)$',
     TeachRecoveryPageView.as_view()),
)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
