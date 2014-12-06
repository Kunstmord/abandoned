from django.contrib import admin
from abandoned.models import Tag, Project, Author, Reason

admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(Author)
admin.site.register(Reason)
