import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from polls.models import Question


# Create your tests here.
class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently())


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(question, text, votes):
    return question.choice_set.create(choice_text=text, votes=votes)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question_with_choice(self):
        question = create_question(question_text="past question", days=-30)
        create_choice(question, 'choice', 0)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], ["<Question: past question>"])

    def test_index_view_with_a_past_question_with_no_choice(self):
        create_question(question_text="past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_future_question_with_choice(self):
        question = create_question(question_text="future question", days=30)
        create_choice(question, 'choice', 0)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_and_a_future_question(self):
        question = create_question(question_text="past question", days=-30)
        create_choice(question, 'choice', 0)
        create_question(question_text='future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past question>'])


class QuestionDetailViewTests(TestCase):
    def test_detail_view_with_a_past_question(self):
        past_question = create_question(question_text='Past question', days=-10)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_with_a_future_question(self):
        future_question = create_question(question_text='Future question', days=10)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)


class QuestionResultsViewTests(TestCase):
    def test_results_view_with_a_past_question(self):
        past_question = create_question(question_text='Past question', days=-10)
        response = self.client.get(reverse('polls:results', args=(past_question.id,)))
        self.assertEqual(response.status_code, 200)

    def test_results_view_with_a_future_question(self):
        future_question = create_question(question_text='Future question', days=10)
        response = self.client.get(reverse('polls:results', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)
