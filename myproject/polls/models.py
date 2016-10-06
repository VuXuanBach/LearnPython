# Create your models here.
from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils.timezone import now


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    choice_count = models.IntegerField(default=0)

    def was_published_recently(self):
        if not self.pub_date:
            return False
        return now() - datetime.timedelta(days=1) <= self.pub_date <= now()
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published Recently?'

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.question.choice_count += 1
        self.question.save()
        super(Choice, self).save()

    def delete(self, using=None):
        pass
        self.question.choice_count -= 1
        if self.question.choice_count < 0:
            self.question.choice_count = 0
        self.question.save()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)

    def __str__(self):
        return self.answer_text
