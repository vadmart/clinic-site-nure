from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from quiz.models import QuestionAnswer
from django.views.decorators.csrf import csrf_exempt
import copy


# Create your views here.
def quiz(request):
    return render(request, template_name="quiz.html", context={})


@csrf_exempt
def questions(request):
    qa_set = QuestionAnswer.objects.all().order_by('question_id')
    response = {}
    dct = {"question": None, "inputType": None, "correctAnswers": [], "incorrectAnswers": [], "chosenAnswers": []}
    for qa in qa_set:
        if qa.question.question_text != dct["question"]:
            if dct["question"] is not None:
                response[qa.question.id - 1] = copy.deepcopy(dct)
                dct["correctAnswers"].clear()
                dct["incorrectAnswers"].clear()
        dct["question"] = qa.question.question_text
        dct["inputType"] = qa.question.input_type.type_name
        if qa.is_answer_correct:
            dct["correctAnswers"].append(qa.answer.answer_text)
        else:
            dct["incorrectAnswers"].append(qa.answer.answer_text)
    response[qa_set[len(qa_set) - 1].question.id] = copy.deepcopy(dct)
    return JsonResponse(response)
