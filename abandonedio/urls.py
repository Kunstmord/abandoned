from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from abandoned.views import TagViewSet, AuthorViewSet, ProjectViewSet, ReasonViewSet, LanguageViewSet, handle_submit, main_page


router = routers.DefaultRouter()
router.register(r'api/tags', TagViewSet)
router.register(r'api/authors', AuthorViewSet)
router.register(r'api/reasons', ReasonViewSet)
router.register(r'api/projects', ProjectViewSet)
router.register(r'api/languages', LanguageViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'abandonedio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', main_page),
    url(r'^', include(router.urls)),
    url(r'^api/submit/', handle_submit),
    url(r'^admin/', include(admin.site.urls)),
)
