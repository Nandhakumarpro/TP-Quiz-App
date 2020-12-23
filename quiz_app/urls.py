from django.urls import path, include
from . import views

app_name = "quiz"

urlpatterns = [
    path( "ques_choice/create/<int:quiz_id>/" ,views.CreateQuesChoice.as_view( ), name= "create-ques_choice"  ) ,
    path( "quiz/create" , views.CreateQuiz.as_view( ), name = "create-quiz") ,
    path( "quiz/list" , views.ListQuiz.as_view() , name="quiz-list" ),
    path( "ques_choice/Student/edit/<int:quiz_id>/<int:question_no>/" , views.QuizViewForStudent.as_view() , name = "ques_choice-view-student") ,
]