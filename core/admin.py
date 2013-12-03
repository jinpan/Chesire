from django.contrib import admin

from chesire.core.models import Answer
from chesire.core.models import AnswerVote
from chesire.core.models import Article
from chesire.core.models import ChesireUser
from chesire.core.models import Question
from chesire.core.models import QuestionVote


admin.site.register(Answer)
admin.site.register(AnswerVote)
admin.site.register(Article)
admin.site.register(ChesireUser)
admin.site.register(Question)
admin.site.register(QuestionVote)

