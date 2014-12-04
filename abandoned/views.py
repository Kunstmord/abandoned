from django.shortcuts import render
from rest_framework import viewsets
from abandoned.models import Project, Tag, Author, Reason
from abandoned.serializers import TagSerializer, ProjectSerializer, AuthorSerializer, ReasonSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ReasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer