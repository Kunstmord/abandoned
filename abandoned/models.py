from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField()


class Reason(models.Model):
    reason = models.CharField(max_length=200)


class Tag(models.Model):
    text = models.CharField(max_length=100)


class Project(models.Model):
    name = models.CharField(max_length=400)
    link = models.URLField()
    author = models.ForeignKey(Author)
    description = models.TextField()
    reason = models.ForeignKey(Reason)
    tags = models.ManyToManyField(Tag)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    date_added = models.DateTimeField()