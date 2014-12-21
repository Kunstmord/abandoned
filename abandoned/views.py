from abandoned.githubapi import get_project_data, AbandonedException, GithubException
from abandoned.models import Project, Tag, Author, Reason, Language
from abandoned.serializers import TagSerializer, ProjectSerializer, ReasonSerializer, AuthorSerializer, LanguageSerializer
from django.db.models import Count, Sum
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from json import loads
from rest_framework import viewsets, status
from rest_framework.decorators import list_route, api_view
from rest_framework.response import Response


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


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    @list_route()
    def votes(self, request):
        return votes_generic(Language, self)

    @list_route()
    def projects(self, request):
        return projects_generic(Language, self)


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


@csrf_protect
@api_view(['POST'])
def handle_submit(request):
    request_data = loads(request.body.decode('utf-8'))
    try:
        project_data = get_project_data(request_data['repo_url'])
    except AbandonedException as e:
        return HttpResponseBadRequest(str(e))
    except GithubException as e:
        return HttpResponse(str(e), status=503)
    repo_name, author_name, language = project_data
    author_url = 'https://github.com/' + author_name
    repo_url = 'https://github.com/' + author_name + '/' + repo_name

    if not Project.objects.filter(link=repo_url).exists():
        curr_reason = Reason.objects.get(id=request_data['reason_id'])
        curr_author, author_created = Author.objects.get_or_create(name=author_name, link=author_url)
        curr_language, language_created = Language.objects.get_or_create(name=language)

        tags_list = []
        for tag_text in request_data['tags']:
            curr_tag, tag_created = Tag.objects.get_or_create(text=tag_text)
            tags_list.append(curr_tag)

        curr_project = Project.objects.create(name=repo_name, link=repo_url, author=curr_author,
                                              description=request_data['description'],
                                              reason=curr_reason, language=curr_language)
        for tag in tags_list:
            curr_project.tags.add(tag)
        curr_project.save()
        serializer = ProjectSerializer(curr_project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return HttpResponseBadRequest("This project is already in the database")