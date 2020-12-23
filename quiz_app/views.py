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

from .support import (
    getNoOfQuesForLinkedQuizId ,getValidQuizzesTitles,getNthQuestionOfQuiz,getChoicesOfQuestion
)

NO_OF_QUESTIONS = 2

class CreateQuesChoice ( View ) :
    template_name = "ques-choices-create-form.html"
    form = QuesChoiceForm
    no_of_questions = NO_OF_QUESTIONS
    context = {"errors" : None , "message" : None }
    def get(self, request,quiz_id ) :
        try :
            Quiz.objects.get ( id = int (quiz_id ) )
            ques_count = getNoOfQuesForLinkedQuizId( int(quiz_id) )
            if ques_count<self.no_of_questions :
                self.context["ques_choices_form"] = self.form ( )
                self.context["quiz_id"] = quiz_id
                return render( request , template_name=self.template_name , context=self.context )
            else :
                return redirect( "quiz:quiz-list" )

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
            return  redirect( "quiz:create-ques_choice" , quiz_id = int (quiz_id) )
        else:
            self.context["errors"] = form.errors["__all__"]
            return render( request , template_name=self.template_name ,context=self.context )

class CreateQuiz ( View ) :
    template_name = "create-quiz.html"
    form = QuizForm
    context = {"errors" : None , "message" : None}
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

class ListQuiz ( View ) :
    template_name= "list-quiz.html"
    context = {"errors" : None , "message" : None }
    no_of_questions = NO_OF_QUESTIONS
    def get ( self, request ) :
        self.context [ "titles" ]  = getValidQuizzesTitles( self.no_of_questions )
        return render( request , template_name=self.template_name , context=self.context )

class QuizViewForStudent( View ) :
    template_name = "student-view-quiz.html"
    context = {"errors": None, "message": None, "Result":False }
    form = QuesChoiceForm
    no_of_questions = NO_OF_QUESTIONS

    def getQuesAndChoices(self ,quiz_id , question_no ) :
        question = getNthQuestionOfQuiz( quiz_id , question_no )
        choices  = getChoicesOfQuestion( question=question )
        self.context[ "question"] = question
        self.context[ "choices" ] = choices
        return (question, choices )

    def get ( self ,request , quiz_id , question_no ) :
        question,choices = self.getQuesAndChoices( quiz_id , question_no  )
        ques_choices_form = self.form ( required=False )
        ques_choices_form.setDataForStudentViewForm( question=question , choices= choices )
        self.context [ "ques_choices_form" ]  = ques_choices_form
        self.context["Result"] = False
        return  render( request , template_name=self.template_name , context=self.context )

    def post( self , request, quiz_id , question_no  ) :
        question, choices = self.getQuesAndChoices(quiz_id, question_no)
        form = self.form ( request.POST,required=False )
        if form.is_valid( ) :
            self.context["Correct"] = False
            for i in range(1, 5):
                if  form.cleaned_data .get( f"is_correct{i}" ) == True :
                    if choices[i-1].is_correct == True :
                        self.context["Correct"] = True
                    self.context["Result"] = True
                    self.context["question_no"] = question_no+1
                    return render( request , template_name=self.template_name , context=self.context )
            else:
                return HttpResponse("<h1>Please Click Middle Of the Button</h1>")
        else :
            return HttpResponse( "<h1>Please Click Middle Of the Button</h1>" )

# class QuestionResultView ( View ) :


