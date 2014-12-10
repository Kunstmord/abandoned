from django.shortcuts import render
from django.db.models import Count, Sum
from rest_framework import viewsets
from abandoned.models import Project, Tag, Author, Reason
from rest_framework.response import Response
from rest_framework.decorators import list_route
from abandoned.serializers import TagSerializer, ProjectSerializer, ReasonSerializer, AuthorSerializer


def votes_generic(model_obj, class_instance):
    votes = model_obj.objects.annotate(votes_total=Sum('projects__upvotes')).order_by('votes_total').reverse()
    page = class_instance.paginate_queryset(votes)
    serializer = class_instance.get_pagination_serializer(page)
    return Response(serializer.data)


def projects_generic(model_obj, class_instance):
    votes = model_obj.objects.annotate(Count('projects')).order_by('projects__count').reverse()
    page = class_instance.paginate_queryset(votes)
    serializer = class_instance.get_pagination_serializer(page)
    return Response(serializer.data)


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @list_route()
    def votes(self, request):
        return votes_generic(Author, self)

    @list_route()
    def projects(self, request):
        return projects_generic(Author, self)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @list_route()
    def votes(self, request):
        return votes_generic(Tag, self)

    @list_route()
    def projects(self, request):
        return projects_generic(Tag, self)


class ReasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer

    @list_route()
    def votes(self, request):
        return votes_generic(Reason, self)

    @list_route()
    def projects(self, request):
        return projects_generic(Reason, self)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @list_route()
    def votes(self, request):
        top = Project.objects.all().order_by('upvotes').reverse()
        page = self.paginate_queryset(top)
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)

    @list_route()
    def latest(self, request):
        latest = Project.objects.all().order_by('date_added').reverse()
        page = self.paginate_queryset(latest)
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)