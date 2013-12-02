from models import User, Wine
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'is_superuser')

class WineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wine
        fields = ('url', 'couleur', 'region', 'appellation', 'domaine', 'cuvee', 
        	'millesime', 'description', 'price', 'description')