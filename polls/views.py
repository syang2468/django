from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Choice, Question, DeepThought
from django.urls import reverse
from django.views import generic
from django.utils import timezone

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

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def deepThought(request):
    model = DeepThought
    template_name = loader.get_template('polls/deepthought.html')
    context = {
        'hi' : "hello"
    }
    print(request.POST)
    if(request.method == "POST"):
        inp_value = request.POST.get('thought')
        newthought = DeepThought(thought_text = inp_value, pub_date = timezone.now())
        newthought.save()
        #DeepThought.objects(inp_value)

    return HttpResponse(template_name.render(context, request))

class deepThoughtList(generic.ListView):
    model = DeepThought
    template_name = ('polls/deepthoughtlist.html')
    #context_object_name = 'deep_thought_list'
    #deepthought_list = DeepThought.objects.order_by('pub_date')


    def get_queryset(self):
        return DeepThought.objects.filter(
           pub_date__lte=timezone.now()
        ).order_by('-pub_date')

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
