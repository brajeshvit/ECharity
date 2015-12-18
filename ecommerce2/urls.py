from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from dashing.utils import router
from registration.backends.default.views import RegistrationView
from ajaxuploader.views import AjaxFileUploader

uploader = AjaxFileUploader()


urlpatterns = [
    # Examples:
    url(r'^messages/', include('django_messages.urls')),
    #url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^contact/$', 'newsletter.views.contact', name='contact'),
    url(r'^history/$', 'products.views.post_history', name='post_history'),
    url(r'^history/add/(?P<pk>[0-9]+)/$', 'products.views.post_detail_history', name='post_detail_history'),
    
    url(r'^about/$', 'ecommerce2.views.about', name='about'),
    url(r'^blank/$', 'ecommerce2.views.blank', name='blank'),  
    url(r'^faq/$', 'ecommerce2.views.faq', name='faq'),
    url(r'^service/$', 'ecommerce2.views.service', name='service'),
    url(r'^term/$', 'ecommerce2.views.term', name='term'),
    url(r'^gallery/$', 'ecommerce2.views.gallery', name='gallery'),
    url(r'^dashboard/$', 'dashboard.views.dashboard', name='dashboard'),
    url(r'^profile/$', 'dashboard.views.profile', name='profile'),
    #url(r'^dashboard/', include(router.urls)),
    url(r'^$', 'products.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
    url(r'^products/', include('products.urls')),
    # Django JET URLS
    url(r'^jet/', include('jet.urls', 'jet')), 
    url(r'^tour/$', 'ecommerce2.views.tour', name='tour'),
    url(r'^avatar/', include('avatar.urls')),

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
