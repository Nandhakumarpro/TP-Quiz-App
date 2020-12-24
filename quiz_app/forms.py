
from django import forms
from django.forms import formset_factory

class QuizForm( forms.Form ) :
    quiz_title = forms.CharField ( max_length=50 ,required=True )

class QuesChoiceForm ( forms.Form ) :
    def __init__(self,*args,**kwargs ) :
        required  = kwargs .pop ( "required" , True )
        super( QuesChoiceForm , self ).__init__( *args,**kwargs )
        self.fields[f"question"] = forms.CharField(max_length=1000, required=required,label="Question")
        for i in range( 1,5 ) :
            self.fields[f"option{i}"] = forms.CharField ( max_length=255, required=required  )
            self.fields[f"is_correct{i}"] = forms.BooleanField( widget=forms.CheckboxInput(attrs={'style':'width:20px;height:20px;'}),required=False,label="is_correct" )

    def clean(self):
        data = self.cleaned_data
        is_correct_list = [data.get(f"is_correct{i}") for i in range(1, 5)]
        if not ( any(is_correct_list) ) :
            raise forms.ValidationError( "You Should select atleast one as correct answer!!!")
        if all(is_correct_list) :
            raise forms.ValidationError("You Should not select all as correct answer!!!")

    def setDataForStudentViewForm ( self , question , choices ) :
        self.fields[f"question"].initial = question.question
        for i in range( 1,5 ) :
            self.fields[f"option{i}"].initial = choices[i-1].choice_desc
            # self.fields[f"is_correct{i}"].initial = forms.BooleanField( widget=forms.CheckboxInput(),required=False,label="is_correct" )

    class Meta :
        fields = "__all__"

class SignUpForm( forms.Form ) :
    username = forms.CharField ( max_length=100, required=True, label= "UserName:" )
    password = forms.CharField ( max_length=20 , required=True, label= "Password:",widget=forms.PasswordInput() )

class LoginForm(SignUpForm ):
    pass


