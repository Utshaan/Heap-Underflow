from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Answer

from .models import Question

def home(request):
    context = {
        'questions': Question.objects.all()
    }
    return render(request, 'forum/home.html', context)

class QuestionListView(ListView):
    model = Question
    template_name = 'forum/home.html'
    context_object_name = 'questions'
    ordering = ['-date_posted']

class QuestionDetailView(DetailView):
    model = Question

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            answer = Answer()
            answer.content = request.POST.get('answer-content')
            answer.author = request.user
            answer.question = self.get_object()
            answer.save()
            return self.get(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['answers'] = self.object.answer_set.order_by('-date_posted').all()
        context['upvotes'] = self.object.crazy_set.all().count()
        context['downvotes'] = self.object.eh_set.all().count()
        return context

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.author

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = '/'

    def test_func(self):
            question = self.get_object()
            return self.request.user == question.author

class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    pk_url_kwarg = 'a_pk'

    def test_func(self):
            answer = get_object_or_404(Answer, pk=self.kwargs.get('a_pk'))
            return self.request.user == answer.author

    def get_context_data(self, **kwargs):
        context = super(AnswerDeleteView, self).get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, pk=self.kwargs.get('q_pk'))
        return context

    def get_success_url(self):
        question = get_object_or_404(Question, pk=self.kwargs.get('q_pk'))
        return question.get_absolute_url()

def upvote(request, pk):
    if Question.objects.filter(id=pk).first().crazy_set.filter(owner=request.user).exists():
        Question.objects.filter(id=pk).first().crazy_set.filter(owner=request.user).delete()
    elif Question.objects.filter(id=pk).first().eh_set.filter(owner=request.user).exists():
        Question.objects.filter(id=pk).first().eh_set.filter(owner=request.user).delete()
        Question.objects.filter(id=pk).first().crazy_set.create(owner=request.user, question_id=pk)
    else:
        Question.objects.filter(id=pk).first().crazy_set.create(owner=request.user, question_id=pk)
    return redirect('question-detail', pk)

def downvote(request, pk):
    if Question.objects.filter(id=pk).first().eh_set.filter(owner=request.user).exists():
        Question.objects.filter(id=pk).first().eh_set.filter(owner=request.user).delete()
    elif Question.objects.filter(id=pk).first().crazy_set.filter(owner=request.user).exists():
        Question.objects.filter(id=pk).first().crazy_set.filter(owner=request.user).delete()
        Question.objects.filter(id=pk).first().eh_set.create(owner=request.user, question_id=pk)
    else:
        Question.objects.filter(id=pk).first().eh_set.create(owner=request.user, question_id=pk)
    return redirect('question-detail', pk)
