from .models import *

def getNoOfQuesForLinkedQuizId ( quiz_id:int ) :
    return  Questions.objects.filter( quiz__id=quiz_id ).count( )

def getValidQuizzesTitles ( check_no ) :
    titles = [ ]
    for quiz in Quiz.objects.all(  ) :
        if getNoOfQuesForLinkedQuizId( quiz.id) == check_no :
            titles.append( quiz.title )
    return titles

def getNthQuestionOfQuiz( quiz_id, question_no ) :
    return  Questions.objects.filter ( quiz__id=quiz_id   ) [ question_no - 1]

def getChoicesOfQuestion( question) :
    return Choices.objects.filter ( question = question  )