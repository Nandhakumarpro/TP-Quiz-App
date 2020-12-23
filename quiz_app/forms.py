
from django import forms
from django.forms import formset_factory

class QuizForm( forms.Form ) :
    quiz_title = forms.CharField ( max_length=50 ,required=True )

class QuesChoiceForm ( forms.Form ) :
    def __init__(self,*args,**kwargs ) :
        super( QuesChoiceForm , self ).__init__( *args,**kwargs )
        self.fields[f"question"] = forms.CharField(max_length=1000, required=True)
        for i in range( 1,5 ) :
            self.fields[f"option{i}"] = forms.CharField ( max_length=255, required=True )
            self.fields[f"is_correct{i}"] = forms.BooleanField( widget=forms.CheckboxInput(),required=False,label="is_correct" )

    def clean(self):
        data = self.cleaned_data
        is_correct_list = [data.get(f"is_correct{i}") for i in range(1, 5)]
        if not ( any(is_correct_list) ) :
            raise forms.ValidationError( "You Should select atleast one as correct answer!!!")
        if all(is_correct_list) :
            raise forms.ValidationError("You Should not select all as correct answer!!!")

    class Meta :
        fields = "__all__"

