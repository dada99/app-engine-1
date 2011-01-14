from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^django/', 'mysite.upload.views.current_datetime'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #('^$', 'django.views.generic.simple.direct_to_template',
     #{'template': 'home.html'}),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
