from django.contrib import admin
from abandoned.models import Tag, Project, Author, Reason, Language

admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(Author)
admin.site.register(Reason)
admin.site.register(Language)