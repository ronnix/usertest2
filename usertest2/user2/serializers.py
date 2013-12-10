from models import User, Wine, Movement, Container, Bottle
from rest_framework import serializers


# class VinibarSerializer(serializers.Serializer):


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
        	'millesime', 'description', 'price', 'quantity')

class MovementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movement
        fields = ('url', 'date', 'start', 'finish', 'quantity')

class ContainerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Container
        fields = ('url', 'container_type', 'user')

class BottleSerializer(serializers.HyperlinkedModelSerializer):

	# def __init__(self, *args, **kwargs):
	# 	many = kwargs.pop('many', True)
	# 	super(BottleSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Bottle
        fields = ('url', 'wine', 'user')

class RatingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Bottle
        fields = ('url', 'rating', 'comment')

	# def get_api_url(self, obj):
	# 	return "#/post/%s" % obj.id