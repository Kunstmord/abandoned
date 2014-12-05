__author__ = 'georgeoblapenko'

from rest_framework import serializers
from abandoned.models import Author, Reason, Tag, Project


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'link',)


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('id', 'reason',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'text',)


class ProjectSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    reason = ReasonSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'link', 'author', 'description', 'reason', 'tags', 'upvotes', 'date_added')