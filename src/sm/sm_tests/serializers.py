from django.contrib.auth.models import User
from .models import (MentalTest, MentalTestField, MentalTestFieldType,
                     MentalTestResult)
from rest_framework import serializers
from rest_framework.renderers import AdminRenderer, JSONRenderer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer class for users
    """
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'first_name', 'last_name', 'password', 'email', 'groups']


class MentalTestFieldTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer class for Mental Test Field Type
    """
    class Meta:
        model = MentalTestFieldType
        fields = ['url', 'id', 'name', 'description', 'initial_range', 'final_range', 'initial_label', 'final_label']


class MentalTestFieldSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer class for Mental Test Field
    """

    field_type = MentalTestFieldTypeSerializer()
    class Meta:
        model = MentalTestField
        fields = ['url', 'id', 'test', 'name', 'description', 'field_type', 'weight']


#class CurrentUser(serializers.RelatedField):
    #def to_representation(self, value):
    #def get_object(self, view_name, view_args, view_kwargs):
    #    user = serializers.CurrentUserDefault()
    #    logger = logging.getLogger(__name__)
    #    logger.info("USER: " + user)
    #    return user

class MentalTestSerializer(serializers.HyperlinkedModelSerializer):
    """
       Serializer class for Mental Test
    """
    mental_test_fields = MentalTestFieldSerializer(many=True, read_only=False)
    current_user = serializers.StringRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault()
    )
    #current_user = CurrentUser(read_only=True)
    #current_user = current_user.name
    class Meta:
        model = MentalTest
        fields = ['url', 'id', 'owner', 'name', 'description', 'mental_test_fields', 'current_user']

    owner = serializers.ReadOnlyField(source='owner.username')


class MentalTestResultSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer class for Mental Test Results
    """
    class Meta:
        model = MentalTestResult
        fields = ['url', 'test', 'user', 'test_field', 'value']

    user = serializers.ReadOnlyField(source='user.username')
