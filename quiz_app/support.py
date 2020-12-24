from .models import *

def getNoOfQuesForLinkedQuizId ( quiz_id:int ) :
    return  Questions.objects.filter( quiz__id=quiz_id ).count( )

def getValidQuizzesTitles ( check_no ) :
    titlesAndids = [ ]
    for quiz in Quiz.objects.all(  ) :
        if getNoOfQuesForLinkedQuizId( quiz.id) == check_no :
            titlesAndids.append( ( quiz.title,  quiz.id )  )
    return  titlesAndids

def getNthQuestionOfQuiz( quiz_id, question_no ) :
    return  Questions.objects.filter ( quiz__id=quiz_id   ) [ question_no - 1]

def getChoicesOfQuestion( question) :
    return Choices.objects.filter ( question = question  )