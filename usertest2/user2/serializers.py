from models import User, Wine, Movement, Container
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'is_superuser')

class WineSerializer(serializers.HyperlinkedModelSerializer):
    # current_user_feedback = serializers.SerializerMethodField('get_user_feedback')

	# def get_user_feedback(self, obj):
	#     user = self.context['request'].user
	#     feedback = Feedback.objects.get(user=user, wine=obj)
	#     serializer = FeedbackSerializer(feedback)
	#     return serializer.data

    class Meta:
        model = Wine
        fields = ('url', 'couleur', 'region', 'appellation', 'domaine', 'cuvee', 
        	'millesime', 'description', 'price', 'description')

class MovementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movement
        fields = ('url', 'date', 'start', 'finish', 'quantity')

class ContainerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Container
        fields = ('url', 'container_type', 'user')