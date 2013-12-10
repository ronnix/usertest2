from django.shortcuts import render
#from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, generics
from models import User, Wine, Movement, Container, Bottle
from serializers import UserSerializer, WineSerializer, MovementSerializer, ContainerSerializer, BottleSerializer, RatingSerializer
#from quickstart.serializers import UserSerializer, GroupSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate, login

from django.http import HttpResponse, HttpResponseRedirect, QueryDict, Http404
from django.template.response import TemplateResponse



# def login(request):
#     if request.method != 'POST':
#         raise Http404('Only POSTs are allowed')
#     try:
#         u = User.objects.get(username=request.POST['username'])
#         if u.password == request.POST['password']:
#             request.session['user_id'] = u.id
#             return HttpResponseRedirect('/vinibarwines/')
#     except User.DoesNotExist:
#         return HttpResponse("Your username and password didn't match.")

# def login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             return redirect('vinibarwines')
#         else:
#             #request.context['status'] = 'inactive user'
#             pass
#     else:
#         #request.context['status'] = 'incorrect login/password'
#         pass


class VinibarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = BottleSerializer

    def get_queryset(self):
    	queryset = Bottle.objects.all()
    	username = self.request.user
    	if username is not None:
    		queryset = queryset.filter(user=username)
		return queryset


class VinibarWinesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = WineSerializer

    def get_queryset(self):
    	username = self.request.user
    	queryset = Wine.objects.filter(bottle__user=username, bottle__rated__isnull=True)
    	return queryset


class RatedWinesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = WineSerializer

    def get_queryset(self):
    	#if request.user.is_authenticated():
		username = self.request.user
		queryset = Wine.objects.filter(bottle__user=username, bottle__rated__isnull=False, bottle__rating__isnull=False)
		return queryset


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

class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bottles to be viewed or edited.
    """
    queryset = Bottle.objects.all()
    serializer_class = BottleSerializer

    # class ExampleView(APIView):
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, format=None):
#         content = {
#             'user': unicode(request.user),  # `django.contrib.auth.User` instance.
#             'auth': unicode(request.auth),  # None
#         }
#         return Response(content)



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