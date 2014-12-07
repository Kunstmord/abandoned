__author__ = 'georgeoblapenko'

from rest_framework import serializers
from abandoned.models import Author, Reason, Tag, Project


class BaseAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'link',)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'link', 'projects')


class BaseReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('id', 'reason',)


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('id', 'reason', 'projects')


class BaseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'text',)


class BaseProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'text', 'projects')


class ProjectSerializer(serializers.ModelSerializer):
    author = BaseAuthorSerializer()
    reason = BaseReasonSerializer()
    tags = BaseTagSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'link', 'author', 'description', 'reason', 'tags', 'upvotes', 'date_added')