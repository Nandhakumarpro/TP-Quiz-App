from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth.models import User

# Create your models here.

class Quiz ( models.Model ) :
    title = models.CharField( max_length=50 , null=False , blank=False )

class Questions ( models.Model ) :
    question = models.CharField( max_length=1000 , null=False,blank=False )
    quiz = models.ForeignKey ( Quiz ,on_delete=models.CASCADE )


class Choices ( models.Model ) :
    choice_desc = models.CharField ( max_length=255 ,null=False ,blank=False )
    is_correct = models.BooleanField ( default=False , blank=True )
    question= models.ForeignKey ( Questions , on_delete=models.CASCADE )

class Student ( models.Model ) :
    username = models.CharField( max_length=100, null=False,blank=False,unique=True )
    password = models.CharField( max_length=255 , null=False ,blank=False,)
    
    def save(self , *args , **kwargs ) :
        self.password = make_password( self.password )
        super(Student, self).save( *args, **kwargs )


class Admin (models.Model):
    username = models.CharField(max_length=100, null=False, blank=False,unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Admin, self).save(*args, **kwargs)


class StudentQuizTrack ( models.Model ) :
    student = models.ForeignKey ( Student , on_delete=models.CASCADE )
    quiz = models.ForeignKey ( Quiz , on_delete=models.CASCADE  )
    questions_completed = models.IntegerField ( default=0 )
    Score = models.FloatField ( default=0.0 )

class StudentQuesAnsTrack(models.Model ) :
    question = models.ForeignKey ( Questions , on_delete=models.CASCADE )
    student_answer = models.IntegerField ( null=False )

@receiver ( post_save , sender =Student )
def create_student_user_acc ( sender , instance = None , created = False , **kwargs ) :
    try:
        if created :
            user = User( )
            user.username =  instance.username
            user.password = instance.password
            user.save()
    except Exception as e :
        instance.delete( )

@receiver ( post_save , sender =Admin )
def create_admin_user_acc ( sender , instance = None , created = False , **kwargs ) :
    try:
        if created :
            user = User( )
            user.username =  instance.username
            user.password = instance.password
            user.is_staff = True
            user.save()
    except Exception as e :
        instance.delete( )