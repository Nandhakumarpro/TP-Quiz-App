from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.forms import formset_factory
from django.http import HttpResponse ,Http404 ,HttpResponseRedirect
from .models import  (
    Quiz , Questions ,Choices
    )
from .forms import (
    QuizForm ,# QuestionForm , ChoiceForm,
    QuesChoiceForm
    )

class CreateQuesChoice ( View ) :
    template_name = "ques-choices-create-form.html"
    form = QuesChoiceForm
    no_of_questions = 2
    context = {"errors" : None }
    def get(self, request,quiz_id ) :
        try :
            Quiz.objects.get ( id = int (quiz_id ) )
            self.context["ques_choices_form"] = self.form ( )
            self.context["quiz_id"] = quiz_id
            return render( request , template_name=self.template_name , context=self.context )
        except Quiz.DoesNotExist :
            return  redirect( "quiz:create-quiz" )

    def post ( self, request, quiz_id ) :
        form = self.form ( request.POST or None )
        self.context["ques_choices_form"] = form
        if form.is_valid ( ):
            data = form.cleaned_data
            question = Questions ( question = data.get(
                "question" ), quiz_id = Quiz.objects.get ( id = int (quiz_id ) )
            )
            question.save( )
            for i in range ( 1 , 5 ) :
                choice:Choices = Choices( )
                choice.choice_desc = data[f"option{i}"]
                choice.is_correct = data[f"is_correct{i}"]
                choice.question_id = question
                choice.save()
            return HttpResponse( "<h1>Successfully Saved</h1>")
        else:
            self.context["errors"] = form.errors["__all__"]
            return render( request , template_name=self.template_name ,context=self.context )

class CreateQuiz ( View ) :
    template_name = "create-quiz.html"
    form = QuizForm
    context = {}
    def get ( self, request ) :
        form = self.form ( )
        self.context[ "quiz_form"] = form
        return  render( request , template_name=self.template_name ,context=self.context )

    def post ( self , request ) :
        form = self.form ( request.POST )
        if form.is_valid( ) :
            quiz = Quiz ( )
            quiz.title = form.cleaned_data["quiz_title"]
            quiz.save( )
            return redirect ( "quiz:create-ques_choice" , quiz_id = quiz.id  )
        else :
            raise Http404


