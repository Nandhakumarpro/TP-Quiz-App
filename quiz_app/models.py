from django.db import models

# Create your models here.

class Quiz ( models.Model ) :
    name = models.CharField( max_length=50 , null=False , blank=False )


class Questions ( models.Model ) :
    question = models.CharField( max_length=1000 , null=False,blank=False )

class Choices ( models.Model ) :
    choice = models.CharField ( max_length=255 ,null=False ,blank=False )
    is_correct = models.BooleanField ( default=False , blank=True )
    question_id = models.ForeignKey ( Questions , on_delete=models.CASCADE )


