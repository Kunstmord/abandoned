import abandoned.views
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'tags', abandoned.views.TagViewSet)
router.register(r'authors', abandoned.views.AuthorViewSet)
router.register(r'reasons', abandoned.views.ReasonViewSet)
router.register(r'projects', abandoned.views.ProjectViewSet)
router.register(r'languages', abandoned.views.LanguageViewSet)

urlpatterns = patterns('',
                       url(r'^$', abandoned.views.main_page, name='main_page'),
                       url(r'^projects/$', abandoned.views.projects_view, name='projects_latest'),
                       url(r'^projects/(?P<sorting>\w+)/$', abandoned.views.projects_view, name='projects'),
                       url(r'^project/(?P<project_id>\d+)/$', abandoned.views.single_project_view, name='project'),
                       url(r'^languages/$', abandoned.views.languages_view, name='languages_alphabetical'),
                       url(r'^languages/(?P<sorting>\w+)/$', abandoned.views.languages_view, name='languages'),
                       url(r'^language/(?P<language_id>\d+)/$', abandoned.views.single_language_view, name='language'),
                       url(r'^tags/$', abandoned.views.tags_view, name='tags_alphabetical'),
                       url(r'^tags/(?P<sorting>\w+)/$', abandoned.views.tags_view, name='tags'),
                       url(r'^tag/(?P<tag_id>\w+)/$', abandoned.views.single_tag_view, name='tag'),
                       url(r'^authors/$', abandoned.views.authors_view, name='authors_alphabetical'),
                       url(r'^authors/(?P<sorting>\w+)/$', abandoned.views.authors_view, name='authors'),
                       url(r'^author/(?P<author_id>\d+)/$', abandoned.views.single_author_view, name='author'),
                       url(r'^reasons/$', abandoned.views.reasons_view, name='reasons_alphabetical'),
                       url(r'^reasons/(?P<sorting>\w+)/$', abandoned.views.reasons_view, name='reasons'),
                       url(r'^reason/(?P<reason_id>\d+)/$', abandoned.views.single_reason_view, name='reason'),
                       url(r'^upvote/$', abandoned.views.handle_upvote, name='upvote'),
                       url(r'^submit/$', abandoned.views.handle_submit, name='submit'),
                       url(r'^api_info/$', abandoned.views.api_info_view, name='api_info'),
                       url(r'^cookies/$', abandoned.views.cookie_info_view, name='cookies'),
                       url(r'^api/', include(router.urls)),
                       url(r'^admin/', include(admin.site.urls)),
                       )