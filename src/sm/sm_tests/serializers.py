from django.contrib.auth.models import User
from .models import (MentalTest, MentalTestField, MentalTestFieldType,
                     MentalTestResult)
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer class for users
    """
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'password', 'email', 'groups']

class MentalTestSerializer(serializers.HyperlinkedModelSerializer):
    """
       Serializer class for Mental Test
    """
    class Meta:
        model = MentalTest
        fields = ['url', 'owner', 'name', 'description']

    owner = serializers.ReadOnlyField(source='owner.username')

class MentalTestFieldTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer class for Mental Test Field Type
    """
    class Meta:
        model = MentalTestFieldType
        fields = ['name', 'description']

class MentalTestFieldSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer class for Mental Test Field
    """
    class Meta:
        model = MentalTestField
        fields = ['url', 'test', 'name', 'description', 'field_type', 'weight']

class MentalTestResultSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer class for Mental Test Results
    """
    class Meta:
        model = MentalTestResult
        fields = ['url', 'test', 'user', 'test_field', 'value']

    user = serializers.ReadOnlyField(source='user.username')
