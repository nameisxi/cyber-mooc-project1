import urllib

from django.utils import timezone

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

    def post(self, request):
        # do some stuff here
        return HttpResponse('Message received!')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def get_poll_by_name(request, question_name):
    question_name = urllib.parse.unquote(question_name).replace('+', ' ')
    print("QUESTION:", question_name)
    query = f'SELECT * FROM polls_question WHERE question_text="{question_name}";'
    question = Question.objects.raw(query)
    # question = Question.objects.filter(question_text=question_name)
    return HttpResponse(question)

class QuestionSearchView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return a question if matching name.
        """
        question_name = urllib.parse.unquote(self.kwargs['question_name']).replace('+', ' ')
        print("QUESTION:", question_name)
        query = f'SELECT * FROM polls_question WHERE question_text="{question_name}";'
        return Question.objects.raw(query)
        # return Question.objects.filter(question_name=question_name)

def my_poll_creator_profile(request, username):
    return User.objects.get(username=username)
    # if request.user.is_authenticated and request.user.username == username:
    #     return User.objects.get(username=username)
    # return HttpResponse('Oops, not allowed to see that!')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
