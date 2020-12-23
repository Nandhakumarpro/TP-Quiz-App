from django.urls import path, include
from . import views

app_name = "quiz"

urlpatterns = [
    path( "ques_choice/create" ,views.CreateQuesChoice.as_view( ), name= "create-ques_choice"  ) ,
    path( "quiz/create" , views.CreateQuiz.as_view( ), name = "create-quiz") ,

]