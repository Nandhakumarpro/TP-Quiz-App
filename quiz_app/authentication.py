from functools import wraps
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import  *

def is_logged_in( function ) :
    @wraps( function )
    def wrap( self, request , *args , **kwargs ) :

        if not request.user.is_anonymous :
            return function ( self,request,*args , **kwargs )
        else :
            return  redirect( "/quiz/home" )
    return wrap

def is_Student( function ) :
    @wraps(function)
    def wrap ( self, request, *args, **kwargs ) :
        if Student.objects.filter( username=request.user.username ).first() :
            return function ( self, request , *args , **kwargs )
        else :
            return HttpResponse ( "<h1>You are not a Student.So, you are not allowed" )
    return wrap

def is_Admin( function ) :
    @wraps(function)
    def wrap ( self, request, *args, **kwargs ) :
        if Admin.objects.filter( username=request.user.username ).first() :
            return function ( self, request , *args , **kwargs )
        else :
            return HttpResponse ( "<h1>You are not a admin.So, you are not allowed" )
    return wrap
