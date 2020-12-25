from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.forms import formset_factory
from django.http import HttpResponse ,Http404 ,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import  (
    Quiz , Questions ,Choices,Student,Admin, StudentQuizTrack,StudentQuesAnsTrack
    )
from .forms import (
    QuizForm ,# QuestionForm , ChoiceForm,
    QuesChoiceForm,SignUpForm, LoginForm
    )
from .support import (
    getNoOfQuesForLinkedQuizId ,getValidQuizzesTitles,getNthQuestionOfQuiz,getChoicesOfQuestion
)
from .authentication import (
    is_logged_in , is_Admin, is_Student
)
import time

NO_OF_QUESTIONS = 2

class CreateQuesChoice ( View ) :
    template_name = "ques-choices-create-form.html"
    form = QuesChoiceForm
    no_of_questions = NO_OF_QUESTIONS
    context = {"errors" : None , "message" : None }


    @is_Admin
    @is_logged_in
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


    @is_Admin
    @is_logged_in
    def post ( self, request, quiz_id ) :
        form = self.form ( request.POST or None )
        self.context["ques_choices_form"] = form
        if form.is_valid ( ):
            data = form.cleaned_data
            question = Questions ( question = data.get(
                "question" ), quiz = Quiz.objects.get ( id = int (quiz_id ) )
            )
            question.save( )
            for i in range ( 1 , 5 ) :
                choice:Choices = Choices( )
                choice.choice_desc = data[f"option{i}"]
                choice.is_correct = data[f"is_correct{i}"]
                choice.question = question
                choice.save()
            return  redirect( "quiz:create-ques_choice" , quiz_id = int (quiz_id) )
        else:
            self.context["errors"] = form.errors["__all__"]
            return render( request , template_name=self.template_name ,context=self.context )

class CreateQuiz ( View ) :
    template_name = "create-quiz.html"
    form = QuizForm
    context = {"errors" : None , "message" : None}

    @is_Admin
    @is_logged_in
    def get ( self, request ) :
        form = self.form ( )
        self.context[ "quiz_form"] = form
        return  render( request , template_name=self.template_name ,context=self.context )

    @is_Admin
    @is_logged_in
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
        self.context [ "titlesAndids"] = getValidQuizzesTitles( self.no_of_questions )
        return render( request , template_name=self.template_name , context=self.context )

class QuizViewForStudent( View ) :
    answer_map = { x:y for x,y in zip( [0,1,2,3] , [ "a","b", "c","d" ] ) }
    template_name = "student-view-quiz.html"
    form = QuesChoiceForm
    no_of_questions = NO_OF_QUESTIONS

    def getQuesAndChoices(self ,quiz_id , question_no , context ) :
        question = getNthQuestionOfQuiz( quiz_id , question_no )
        choices  = getChoicesOfQuestion( question=question )
        context[ "question"] = question
        context[ "choices" ] = choices
        return (question, choices )

    @is_Student
    @is_logged_in
    def get ( self ,request , quiz_id , question_no ) :
        context = {"errors": None, "message": None, "Result": False}
        sqt, created = StudentQuizTrack.objects.get_or_create(student=self.student,
                                                              quiz=Quiz.objects.get(id=quiz_id))
        sqt.save( )
        if ( question_no-1 >= sqt.questions_completed) :
            if  question_no-1!=sqt.questions_completed :
                messages.error( request , "You Should Complete the Question One By One" )
            question_no = sqt.questions_completed+1
            context["quiz_id"] = quiz_id
            question,choices = self.getQuesAndChoices( quiz_id , question_no ,context=context )
            ques_choices_form = self.form ( required=False )
            ques_choices_form.setDataForStudentViewForm( question=question , choices= choices )
            context [ "ques_choices_form" ]  = ques_choices_form
            context["Result"] = False
            return  render( request , template_name=self.template_name , context=context )
        else :
            context["Result"] = True
            question, choices = self.getQuesAndChoices(quiz_id, question_no,context=context)
            context["question_no"] = question_no + 1
            sqat = StudentQuesAnsTrack.objects.get( student =self.student, question = question )
            context["student_clicked"] = sqat.student_answer + 1
            context["next_url"] =self.getNextUrl( quiz_id=quiz_id , question_no= question_no )
            return render(request, template_name=self.template_name, context=context)
    @is_Student
    @is_logged_in
    def post( self , request, quiz_id , question_no  ) :
        context = {"errors": None, "message": None, "Result": False}
        context["quiz_id"] = quiz_id
        question, choices = self.getQuesAndChoices(quiz_id, question_no, context=context )
        form = self.form ( request.POST,required=False )
        if form.is_valid( ) :
            context["Correct"] = False
            for i in range(1, 5):

                if  form.cleaned_data .get( f"is_correct{i}" ) == True :
                    sqt, created = StudentQuizTrack.objects.get_or_create(student=self.student,
                                                                          quiz=Quiz.objects.get(id=quiz_id))
                    sqt.questions_completed += 1
                    sqt.end_time = time.time()
                    sqat:StudentQuesAnsTrack = StudentQuesAnsTrack ( )
                    sqat.student = self.student
                    sqat.question = getNthQuestionOfQuiz( quiz_id, question_no=question_no )
                    sqat.student_answer = i - 1
                    sqat.save( )
                    if choices[i-1].is_correct == True :
                        context["Correct"] = True
                        sqt.score+=1
                    sqt.save()
                    context["Result"] = True
                    context["question_no"] = question_no+1
                    context["student_clicked"] =  sqat.student_answer + 1
                    context["next_url"] =self.getNextUrl( quiz_id=quiz_id , question_no= question_no )
                    return render( request , template_name=self.template_name , context=context )
            else:
                return HttpResponse("<h1>Please Click Middle Of the Button</h1>")
        else :
            return HttpResponse( "<h1>Please Click Middle Of the Button</h1>" )
    def getNextUrl(self ,quiz_id, question_no ) :
        return  (f"/quiz/ques_choice/Student/edit/{quiz_id}/{question_no + 1}/" if
                                                question_no + 1 <= NO_OF_QUESTIONS else f"/quiz/report/student/{quiz_id}")

def home ( request ):
    context = { }
    context["links"] = [
        {"label":'Quiz List' , "url":"/quiz/quiz/list"} ,
        {"label":"Login " , "url" :"/quiz/login"} ,
        {"label":"Signup Student " , "url":"/quiz/signup/student"},
        {"label":"Signup Admin" , "url":"/quiz/signup/admin"} ,
        {"label":"Create Quiz" , "url":"/quiz/quiz/create"} ,
    ]
    return render ( request , "home.html" , context=context )

class SignUpStudent( View ) :
    form = SignUpForm
    template_name = "signup.html"
    context = { "form_title":"SignUp Form -Student" }
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
                    return redirect( "/quiz/login")
                else :
                    return HttpResponse("<h1>Username Conflict is there.Try another One!!!")
            except  :
                return HttpResponse("<h1>Username Conflict is there.Try another One!!!")
        else:
            self.context[ "errors" ] = form.errors["__all__"]
            return  render( request , self.template_name , self.context  )

class SignUpAdmin(SignUpStudent ) :
    model = Admin
    context = {"form_title": "SignUp Form -Admin"}
    '''
    In Super class post method student will be replaced by admin 
    
    '''

class Login( View ) :
    template_name = "signup.html" #SignUp Form used here for login
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
                return redirect( "/quiz/home" )
            else :
                messages.error( request , "Your Credentials are Wrong .Please enter again right!!!" )
                return render(request, self.template_name, self.context)
        else :
            self.context["errors"] = form.errors["__all__"]
            return render(request, self.template_name, self.context)

class StudentTestReport( View ) :
    template_name = "student-test-report.html"
    @is_Student
    @is_logged_in
    def get(self , request,  quiz_id ) :
        context = {"test_completed": False}
        quiz = Quiz.objects.get(id=quiz_id)
        sqt = StudentQuizTrack.objects.filter( student = self.student, quiz =quiz ).first()
        if sqt:
            if sqt.questions_completed == NO_OF_QUESTIONS :
                context[  "test_completed"] = True
                context [ "score"] = sqt.score
                context [ "time_taken" ] =sqt.end_time -sqt.start_time
                context [ "title" ] = quiz.title
                context [ "NO_OF_QUESTIONS" ]= NO_OF_QUESTIONS
        else:
            messages.error( request , "You Are Not taken the this Quiz till..." )
        return render ( request , self.template_name , context  )

