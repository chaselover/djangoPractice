# from django import template
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
# from django.template import loader
# 숏컷으로 render 사용. template에 context를 채워넣어 표현한 경과를 HttpResponse객체와 함꼐 돌려주는 구문. render
from django.shortcuts import render,get_object_or_404
# from django.http import Http404
from django.urls import reverse

from .models import Question,Choice

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html',context)

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question doex not exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html',{'question':question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST는 키로 전송된 자료에 접근할 수 있게 해주는 dictionary객체
        # 선택딘 설문의 id를 문자열로 반환함.
        # 선택된 자료에 choice가 없으면 키에러 발생. rerendering.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 에러나면 질의 창 다시 렌더링 시킴.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Wou didn't choose",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 사용자가 재전송될 URL을 받음.항상 성공적인 처리후에 반환시켜줘야함.
        # reverse호출은 뷰이름, URL패턴 변수를 조합해 '/polls/3/results'를 만듬.
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))