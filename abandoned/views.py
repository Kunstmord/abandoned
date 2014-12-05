from django.shortcuts import render
from rest_framework import viewsets
from abandoned.models import Project, Tag, Author, Reason
from rest_framework.response import Response
from rest_framework.decorators import list_route
from abandoned.serializers import BaseTagSerializer, ProjectSerializer, BaseAuthorSerializer, BaseReasonSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = BaseAuthorSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = BaseTagSerializer


class ReasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reason.objects.all()
    serializer_class = BaseReasonSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @list_route()
    def top(self, request):
        top = Project.objects.all().order_by('upvotes').reverse()
        page = self.paginate_queryset(top)
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)