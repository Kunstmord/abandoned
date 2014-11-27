from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    reason = models.TextField()
    author_link = models.URLField()
    link = models.URLField()
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()


class Tag(models.Model):
    text = models.CharField(max_length=100)