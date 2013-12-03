from django.contrib.auth.models import User 
from django.db import models


class ChesireUser(models.Model):
    email = models.EmailField()
    user = models.OneToOneField(User)

class Vote(models.Model):
    user = models.ForeignKey('ChesireUser')
    VOTE_CHOICES = (
        ('UP', 'Up'),
        ('DOWN', 'Down'),
    )
    vote = models.CharField(choices=VOTE_CHOICES,
                            max_length=4)
    time = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class QuestionVote(Vote):
    question = models.ForeignKey('Question')

class AnswerVote(Vote):
    answer = models.ForeignKey('Answer')

class Question(models.Model):
    text = models.TextField()
    article = models.ForeignKey('Article')

    def __unicode__(self):
        return self.text

class Answer(models.Model):
    user = models.ForeignKey('ChesireUser')
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey('Question')

    def __unicode__(self):
        return self.text
    
class Article(models.Model):
    url = models.URLField()
    text = models.TextField()

