from django.shortcuts import render, redirect
from django.views.generic import View
from django.forms import formset_factory
from django.http import HttpResponse ,Http404
from .models import  (
    Quiz , Questions ,Choices
    )

from .forms import (
    QuizForm ,# QuestionForm , ChoiceForm,
    QuesChoiceForm
    )
# Create your views here.

class CreateQuesChoice ( View ) :
    template_name = "ques-choices-create-form.html"
    form = QuesChoiceForm
    no_of_questions = 2
    def get(self, request ) :
        quiz_id = request.GET.get( "quiz_id" , None )
        if quiz_id :
            try :
                Quiz.objects.get ( id = quiz_id )
                context ={ }
                context["ques_choices_form"] = self.form ( )
                return render( request , template_name=self.template_name , context=context )
            except Quiz.DoesNotExist :
                raise  Http404
        else :
            return  redirect( "" )

    def post ( self, request ) :
        context = { }
        form = self.form ( request.POST or None )
        if form.is_valid ( ):
            print(form.cleaned_data)
        else:
            print ( form.errors )
        return HttpResponse ( "<h1>It is Successful</h1>" )

class CreateQuiz ( View ) :
    template_name = "create-quiz.html"
    def get ( self, request ) :
        pass 


