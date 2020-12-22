
from django import forms

class QuizForm( forms.Form ) :
    quiz_title = forms.CharField ( max_length=50 ,required=True )

class QuestionForm(forms.Form ) :
    question = forms.CharField ( max_length=1000, required=True  )

class ChoiceForm(forms.Form ) :
    option = forms.CharField ( max_length=255, required=True )
    is_correct = forms.BooleanField( widget=forms.CheckboxInput() )



