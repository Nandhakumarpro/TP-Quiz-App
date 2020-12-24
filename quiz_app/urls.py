from django.urls import path, include
from . import views

app_name = "quiz"

urlpatterns = [
    path( "home" , views.home , name="home") ,
    path( "ques_choice/create/<int:quiz_id>/" ,views.CreateQuesChoice.as_view( ), name= "create-ques_choice"  ) ,
    path( "quiz/create" , views.CreateQuiz.as_view( ), name = "create-quiz") ,
    path( "quiz/list" , views.ListQuiz.as_view() , name="quiz-list" ),
    path( "ques_choice/Student/edit/<int:quiz_id>/<int:question_no>/" , views.QuizViewForStudent.as_view() , name = "ques_choice-view-student") ,
    path( "signup/student" , views.SignUpStudent.as_view() , name="signup-student") ,
    path( "signup/admin" , views.SignUpAdmin.as_view( ), name="signup-admin" ) ,
    path( "login", views.Login.as_view() , name ="login" ),
    path( "report/student/<int:quiz_id>", views.StudentTestReport.as_view() , name ="student-quiz-report" )

]