import abandoned.views
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'api/tags', abandoned.views.TagViewSet)
router.register(r'api/authors', abandoned.views.AuthorViewSet)
router.register(r'api/reasons', abandoned.views.ReasonViewSet)
router.register(r'api/projects', abandoned.views.ProjectViewSet)
router.register(r'api/languages', abandoned.views.LanguageViewSet)

urlpatterns = patterns('',
                       url(r'^$', abandoned.views.main_page),
                       url(r'^projects/$', abandoned.views.projects_view),
                       url(r'^projects/(?P<sorting>\w+)/$', abandoned.views.projects_view),
                       url(r'^languages/$', abandoned.views.languages_view),
                       url(r'^languages/(?P<sorting>\w+)/$', abandoned.views.languages_view),
                       url(r'^', include(router.urls)),
                       url(r'^api/submit/$', abandoned.views.handle_submit),
                       url(r'^admin/', include(admin.site.urls)),
                       )
