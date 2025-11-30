from django.shortcuts import render
from rest_framework import generics 
from .serializers import Transaction

class ListCreateaApiView (generics.ListAPIView):
    serializer_class = Transaction
    
    
