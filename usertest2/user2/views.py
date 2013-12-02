from django.shortcuts import render
#from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from models import User #Feedback, Wine
from serializers import UserSerializer #FeedbackSerializer, WineSerializer
#from quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer