from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField()

    def __str__(self):
        return str(self.name)


class Reason(models.Model):
    reason = models.CharField(max_length=200)

    def __str__(self):
        return str(self.reason)


class Tag(models.Model):
    text = models.CharField(max_length=100)

    def __str__(self):
        return str(self.text)


class Project(models.Model):
    name = models.CharField(max_length=400)
    link = models.URLField()
    author = models.ForeignKey(Author)
    description = models.TextField()
    reason = models.ForeignKey(Reason)
    tags = models.ManyToManyField(Tag)
    upvotes = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)