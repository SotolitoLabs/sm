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
        fields = ['url', 'id', 'name', 'description']


class MentalTestFieldSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer class for Mental Test Field
    """
    class Meta:
        model = MentalTestField
        fields = ['url', 'id', 'test', 'name', 'description', 'field_type', 'weight']


class MentalTestSerializer(serializers.HyperlinkedModelSerializer):
    """
       Serializer class for Mental Test
    """
    #renderer_classes = [AdminRenderer]
    #renderer_classes = [JSONRenderer]
    #renderer_classes = [PlainTextRenderer]
    mental_test_fields = MentalTestFieldSerializer(many=True, read_only=False)
    #user = "TEST_USER"

    class Meta:
        model = MentalTest
        #fields = ['user', 'url', 'id', 'owner', 'name', 'description', 'mental_test_fields']
        fields = ['url', 'id', 'owner', 'name', 'description', 'mental_test_fields']
        #read_only_fields = ['user']


    owner = serializers.ReadOnlyField(source='owner.username')

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs


class MentalTestResultSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer class for Mental Test Results
    """
    class Meta:
        model = MentalTestResult
        fields = ['url', 'test', 'user', 'test_field', 'value']

    user = serializers.ReadOnlyField(source='user.username')
