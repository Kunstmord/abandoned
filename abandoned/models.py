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


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Project(models.Model):
    name = models.CharField(max_length=400)
    link = models.URLField()
    author = models.ForeignKey(Author, related_name='projects')
    description = models.TextField()
    reason = models.ForeignKey(Reason, related_name='projects')
    language = models.ForeignKey(Language, related_name='projects')
    tags = models.ManyToManyField(Tag, related_name='projects')
    upvotes = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)