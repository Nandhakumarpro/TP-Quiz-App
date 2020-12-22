from django.urls import path, include
from . import views

app_name = "quiz"

urlpatterns = [
    path( "create-quiz" ,views.CreateQuiz.as_view() , name= "create-quiz"  )
]