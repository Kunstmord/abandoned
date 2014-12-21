__author__ = 'georgeoblapenko'

from rest_framework import serializers
from abandoned.models import Author, Reason, Tag, Project, Language


class BaseProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'link', 'upvotes')


class BaseAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'link',)


class AuthorSerializer(serializers.ModelSerializer):
    projects = BaseProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'link', 'projects')


class BaseReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('id', 'reason',)


class ReasonSerializer(serializers.ModelSerializer):
    projects = BaseProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Reason
        fields = ('id', 'reason', 'projects')


class BaseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'text',)


class TagSerializer(serializers.ModelSerializer):
    projects = BaseProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'text', 'projects')


class BaseLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name',)


class LanguageSerializer(serializers.ModelSerializer):
    projects = BaseProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Language
        fields = ('id', 'name', 'projects')


class ProjectSerializer(serializers.ModelSerializer):
    author = BaseAuthorSerializer()
    reason = BaseReasonSerializer()
    language = BaseLanguageSerializer()
    tags = BaseTagSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'link', 'author', 'description', 'reason', 'tags', 'language', 'upvotes', 'date_added')