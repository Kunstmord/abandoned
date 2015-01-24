from abandoned.githubapi import get_project_data, AbandonedException, GithubException
from abandoned.forms import ProjectForm
from abandoned.models import Project, Tag, Author, Reason, Language
from abandoned.serializers import TagSerializer, ProjectSerializer, ReasonSerializer, AuthorSerializer, LanguageSerializer
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Sum
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets
from rest_framework.decorators import list_route
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


def pagination_generic(page, sorting, model_obj, sql_lowercase, lowercase_name):
    if sorting == 'projects':
        result_list = model_obj.objects.annotate(votes_total=Sum('projects__upvotes'),
                                                 projects_total=Count('projects')).\
            order_by('projects_total').reverse()
    elif sorting == 'votes':
        result_list = model_obj.objects.annotate(votes_total=Sum('projects__upvotes'),
                                                 projects_total=Count('projects')).order_by('votes_total').reverse()
    else:
        result_list = model_obj.objects.annotate(votes_total=Sum('projects__upvotes'),
                                                 projects_total=Count('projects')).\
            extra(select={lowercase_name: sql_lowercase}).order_by(lowercase_name)
    paginator = Paginator(result_list, 10)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result


def simple_pagination_generic(page, instance_list):
    paginator = Paginator(instance_list, 10)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.extra(select={'lowercase_name': 'lower(name)'}).order_by('lowercase_name')
    serializer_class = AuthorSerializer

    @list_route()
    def votes(self, request):
        return votes_generic(Author, self)

    @list_route()
    def projects(self, request):
        return projects_generic(Author, self)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.extra(select={'lowercase_text': 'lower(text)'}).order_by('lowercase_text')
    serializer_class = TagSerializer

    @list_route()
    def votes(self, request):
        return votes_generic(Tag, self)

    @list_route()
    def projects(self, request):
        return projects_generic(Tag, self)


class ReasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reason.objects.extra(select={'lowercase_reason': 'lower(reason)'}).order_by('lowercase_reason')
    serializer_class = ReasonSerializer

    @list_route()
    def votes(self, request):
        return votes_generic(Reason, self)

    @list_route()
    def projects(self, request):
        return projects_generic(Reason, self)


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.extra(select={'lowercase_name': 'lower(name)'}).order_by('lowercase_name')
    serializer_class = LanguageSerializer

    @list_route()
    def votes(self, request):
        return votes_generic(Language, self)

    @list_route()
    def projects(self, request):
        return projects_generic(Language, self)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.extra(select={'lowercase_name': 'lower(name)'}).order_by('lowercase_name')
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


def handle_submit(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            repo_url = form.cleaned_data['link']
            try:
                project_data = get_project_data(repo_url)
            except AbandonedException as e:
                return render(request, 'submit.html', {'form': form, 'error_message': e.args[0]})
            except GithubException as e:
                return render(request, 'submit.html', {'form': form, 'error_message': e.args[0]})
            repo_name, author_name, language = project_data
            if language is None:
                language = 'Language not specified'
            author_url = 'https://github.com/' + author_name
            repo_url = 'https://github.com/' + author_name + '/' + repo_name

            # if not Project.objects.filter(link=repo_url).exists():
            curr_author, author_created = Author.objects.get_or_create(author_name=author_name,
                                                                       author_link=author_url)
            curr_language, language_created = Language.objects.get_or_create(language_name=language)

            tags_list = form.cleaned_data['tags_textfield'].split(',')

            for i, tag_text in enumerate(tags_list):
                tag_text = tag_text.strip()
                tags_list[i] = tag_text
                curr_tag, tag_created = Tag.objects.get_or_create(text=tag_text)
                tags_list[i] = curr_tag

            curr_project = Project.objects.create(name=repo_name, link=repo_url, author=curr_author,
                                                  description=form.cleaned_data['description'],
                                                  reason=form.cleaned_data['reason'], language=curr_language)
            for tag in tags_list:
                curr_project.tags.add(tag)
            return HttpResponseRedirect(reverse('abandoned.views.single_project_view', args=(curr_project.id,)))
            # else:
            #     prj_id = Project.objects.get(link=repo_url).id
            #     err_msg = 'This project is already in the database'
            #     return render(request, 'submit.html', {'form': form, 'error_message': err_msg,
            #                                            'prj_id': prj_id})
        else:
            return render(request, 'submit.html', {'form': form, 'render_other_errors': True})
    else:
        form = ProjectForm()
        return render(request, 'submit.html', {'form': form})


def handle_upvote(request):
    if request.method == 'POST':
        try:
            project = Project.objects.get(id=request.POST['id'])
            project.upvotes += 1
            project.save()
            return JsonResponse({'upvotes': project.upvotes}, status=200)
        except Project.DoesNotExist:
            raise Http404


@ensure_csrf_cookie
def single_project_view(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise Http404
    return render(request, 'single_project.html', {'project': project})


def single_author_view(request, author_id):
    try:
        page = request.GET.get('page')
        author = Author.objects.annotate(votes_total=Sum('projects__upvotes'),
                                         projects_total=Count('projects')).prefetch_related('projects').get(id=author_id)
    except Author.DoesNotExist:
        raise Http404
    return render(request, 'single_author.html', {'author': author,
                                                  'projects_list': simple_pagination_generic(page, author.projects.all())})


def single_language_view(request, language_id):
    try:
        page = request.GET.get('page')
        language = Language.objects.annotate(votes_total=Sum('projects__upvotes'),
                                             projects_total=Count('projects')).get(id=language_id)
    except Language.DoesNotExist:
        raise Http404
    return render(request, 'single_language.html',
                  {'language': language, 'projects_list': simple_pagination_generic(page, language.projects.all())})


def single_tag_view(request, tag_id):
    try:
        page = request.GET.get('page')
        tag = Tag.objects.annotate(votes_total=Sum('projects__upvotes'),
                                   projects_total=Count('projects')).get(id=tag_id)
    except Tag.DoesNotExist:
        raise Http404
    return render(request, 'single_tag.html', {'tag': tag,
                                               'projects_list': simple_pagination_generic(page, tag.projects.all())})


def single_reason_view(request, reason_id):
    try:
        page = request.GET.get('page')
        reason = Reason.objects.annotate(votes_total=Sum('projects__upvotes'),
                                         projects_total=Count('projects')).get(id=reason_id)
    except Reason.DoesNotExist:
        raise Http404
    return render(request, 'single_reason.html', {'reason': reason,
                                                  'projects_list': simple_pagination_generic(page,
                                                                                             reason.projects.all())})


def languages_view(request, sorting='alphabetical'):
    page = request.GET.get('page')
    return render(request, 'languages.html', {'languages_list': pagination_generic(page, sorting, Language,
                                                                                   'lower(language_name)',
                                                                                   'lowercase_name'),
                                              'sorting': sorting})


def tags_view(request, sorting='alphabetical'):
    page = request.GET.get('page')
    return render(request, 'tags.html', {'tags_list': pagination_generic(page, sorting, Tag, 'lower(text)',
                                                                         'lowercase_text'),
                                         'sorting': sorting})


def authors_view(request, sorting='alphabetical'):
    page = request.GET.get('page')
    return render(request, 'authors.html', {'authors_list': pagination_generic(page, sorting,
                                                                               Author, 'lower(author_name)',
                                                                               'lowercase_name'),
                                            'sorting': sorting})


def projects_view(request, sorting='latest'):
    page = request.GET.get('page')
    if sorting == 'latest':
        projects_list = Project.objects.order_by('date_added').reverse()
    elif sorting == 'votes':
        projects_list = Project.objects.order_by('upvotes').reverse()
    else:
        projects_list = Project.objects.extra(select={'lowercase_name': 'lower(name)'}).order_by('lowercase_name')
    paginator = Paginator(projects_list, 10)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'projects.html', {'projects_list': projects, 'sorting': sorting})


def reasons_view(request, sorting='alphabetical'):
    page = request.GET.get('page')
    return render(request, 'reasons.html', {'reasons_list': pagination_generic(page, sorting,
                                                                               Reason, 'lower(reason)',
                                                                               'lowercase_text'),
                                            'sorting': sorting})


def main_page(request):
    return render(request, 'index.html')