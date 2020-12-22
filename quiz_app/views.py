from django.shortcuts import render
from django.views.generic import View
from django.forms import formset_factory
from django.http import HttpResponse

from .forms import (
    QuizForm , QuestionForm , ChoiceForm
    )
# Create your views here.

class CreateQuiz ( View ) :
    template_name = "quiz-create-form.html"
    no_of_questions = 2
    question_formset = formset_factory( QuestionForm ,extra=no_of_questions )
    choice_formset = formset_factory( ChoiceForm , extra=(4*no_of_questions) )
    def get(self, request ) :
        context ={ }
        quiz_form = QuizForm( )
        context["quiz_form"] = quiz_form
        questions_formset = self.question_formset( )
        context["questions_formset"] = questions_formset
        choices_formset = self.choice_formset( )
        context["choices_formset"] = choices_formset
        context["questions_and_choices"] =  [ ( questions_formset[count] , choices_formset [(count*4):(count+1)*4]) for count in range(self.no_of_questions) ]
        return render( request , template_name=self.template_name , context=context )

    def post ( self, request ) :
        quiz_form = QuizForm( request.POST or None )
        questions_formset = self.question_formset ( request.POST or None )
        choices_formset = self.choice_formset( request.POST or None  )
        if quiz_form.is_valid() :
            if choices_formset.is_valid() :
                for c in choices_formset :
                    print ( c.cleaned_data  )
            else :
                print ( choices_formset.errors )
            print ( quiz_form.cleaned_data["quiz_title"] )
            return HttpResponse ( "<h1>It is Successful</h1>" )
        else:
            return HttpResponse ( f'<h1>{quiz_form.errors}</h1>' )


