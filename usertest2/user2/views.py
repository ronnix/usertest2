from django.shortcuts import render
#from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, generics
from models import User, Wine, Movement, Container, Bottle
from serializers import UserSerializer, WineSerializer, MovementSerializer, ContainerSerializer, BottleSerializer
#from quickstart.serializers import UserSerializer, GroupSerializer


# class VinibarView(generics.ListAPIView):
#     serializer_class = BottleSerializer

#     def get_queryset(self):
#         """
#         This view should return a list of wines in the user's vinibar
#         """
#         queryset = Bottle.objects.all()
#         username = self.request.QUERY_PARAMS.get('email', None)
#         if username is not None:
#             queryset = queryset.filter(user=username)
#         return queryset

class VinibarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = BottleSerializer

    def get_queryset(self):
    	queryset = Bottle.objects.all()
		username = self.request.QUERY_PARAMS.get('email', None)
        if username is not None:
			queryset = queryset.filter(user=username)
		return queryset

# class VinibarViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that shows users vinibars
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def list(self, request):
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = User.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

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

class BottleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bottles to be viewed or edited.
    """
    queryset = Bottle.objects.all()
    serializer_class = BottleSerializer