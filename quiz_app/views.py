from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.forms import formset_factory
from django.http import HttpResponse ,Http404 ,HttpResponseRedirect
from django.contrib import messages

from .models import  (
    Quiz , Questions ,Choices,Student,Admin
    )
from .forms import (
    QuizForm ,# QuestionForm , ChoiceForm,
    QuesChoiceForm,SignUpForm, LoginForm
    )
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import  User
from .support import (
    getNoOfQuesForLinkedQuizId ,getValidQuizzesTitles,getNthQuestionOfQuiz,getChoicesOfQuestion
)
from .authentication import (
    is_logged_in , is_Admin, is_Student
)

NO_OF_QUESTIONS = 2

class CreateQuesChoice ( View ) :
    template_name = "ques-choices-create-form.html"
    form = QuesChoiceForm
    no_of_questions = NO_OF_QUESTIONS
    context = {"errors" : None , "message" : None }

    @is_logged_in
    @is_Admin
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

    @is_logged_in
    @is_Admin
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

    @is_logged_in
    @is_Admin
    def get ( self, request ) :
        form = self.form ( )
        self.context[ "quiz_form"] = form
        return  render( request , template_name=self.template_name ,context=self.context )

    @is_logged_in
    @is_Admin
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

    @is_logged_in
    @is_Student
    def get ( self ,request , quiz_id , question_no ) :
        question,choices = self.getQuesAndChoices( quiz_id , question_no  )
        ques_choices_form = self.form ( required=False )
        ques_choices_form.setDataForStudentViewForm( question=question , choices= choices )
        self.context [ "ques_choices_form" ]  = ques_choices_form
        self.context["Result"] = False
        return  render( request , template_name=self.template_name , context=self.context )

    @is_logged_in
    @is_Student
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

def home ( request ):
    return HttpResponse("<h1>Welcome To Home Page!!!</h1>")

class SignUpStudent( View ) :
    form = SignUpForm
    template_name = "signup.html"
    context = { "form_title":"SignUp Form" }
    model = Student
    def get ( self, request ) :
        self.context["form"] = self.form( )
        return render( request , template_name=self.template_name , context=self.context )

    def post(self,request ) :
        self.context["form"]= form = self.form( request.POST or None )
        if form.is_valid() :
            data = form.cleaned_data
            username = data["username"]
            password = data ["password"]
            student = self.model ( )
            student.username = username
            student.password = password
            try :
                student.save( )
                if self.model.objects.filter( username=username ).first() :
                    return HttpResponse("<h1>SuccessFully Created!!!")
                else :
                    return HttpResponse("<h1>Username Conflict is there.Try another One!!!")
            except  :
                return HttpResponse("<h1>Username Conflict is there.Try another One!!!")
        else:
            self.context[ "errors" ] = form.errors["__all__"]
            return  render( request , self.template_name , self.context  )

class SignUpAdmin(SignUpStudent ) :
    model = Admin
    '''
    In Super class post method student will be replaced by admin 
    
    '''

class Login( View ) :
    template_name = "signup.html" #Same Form used here
    context = { "form_title":"Login Form" }
    form = LoginForm
    def get ( self, request ) :
        self.context["form"] = self.form( )
        return render( request , self.template_name, self.context )
    def post(self,request ) :
        self.context["form"] =form = self.form( request.POST or None )
        if form.is_valid( ) :
            data = form.cleaned_data
            username = data["username"]
            password = data ["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None :
                login ( request , user )
            else :
                messages.error( request , "Your Credentials are Wrong .Please enter again right!!!" )
                return render(request, self.template_name, self.context)
        else :
            self.context["errors"] = form.errors["__all__"]
            return render(request, self.template_name, self.context)

