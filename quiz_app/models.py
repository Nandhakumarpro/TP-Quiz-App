from django.db import models

# Create your models here.

class Quiz ( models.Model ) :
    title = models.CharField( max_length=50 , null=False , blank=False )

class Questions ( models.Model ) :
    question = models.CharField( max_length=1000 , null=False,blank=False )
    quiz_id = models.ForeignKey ( Quiz ,on_delete=models.CASCADE )


class Choices ( models.Model ) :
    choice = models.CharField ( max_length=255 ,null=False ,blank=False )
    is_correct = models.BooleanField ( default=False , blank=True )
    question_id = models.ForeignKey ( Questions , on_delete=models.CASCADE )




