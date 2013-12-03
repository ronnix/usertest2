from django.shortcuts import render
#from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from models import User, Wine, Movement, Container
from serializers import UserSerializer, WineSerializer, MovementSerializer, ContainerSerializer
#from quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class WineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows wines to be viewed or edited.
    """
    queryset = Wine.objects.all()
    serializer_class = WineSerializer

class MovementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows movements to be viewed or edited.
    """
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer

class ContainerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows containers to be viewed or edited.
    """
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer