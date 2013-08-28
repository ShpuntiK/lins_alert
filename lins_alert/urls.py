from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'app.views.index', name='index'),
	url(r'^settings/$', 'app.views.settings', name='settings'),
	url(r'^contacts/$', 'app.views.contacts', name='contacts'),
	url(r'^sign_in/$', 'app.views.signIn', name='signIn'),
	url(r'^sign_up/$', 'app.views.signUp', name='signUp'),
	url(r'^sign_out/$', 'app.views.signOut', name='signOut'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)
