from django.forms import ModelForm, CharField
from abandoned.models import Project


class ProjectForm(ModelForm):
    tags_textfield = CharField()

    class Meta:
        model = Project
        fields = ['link', 'description', 'reason']