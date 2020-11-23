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
        #fields = ['url', 'id', 'username', 'first_name', 'last_name', 'password', 'email', 'groups']
        fields = ['url', 'id', 'username', 'first_name', 'last_name', 'password', 'email']


class MentalTestFieldTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer class for Mental Test Field Type
    """
    class Meta:
        model = MentalTestFieldType
        fields = ['url', 'id', 'name', 'description', 'initial_range', 'final_range', 'initial_label', 'final_label']


class MentalTestFieldUserResultSerializer(serializers.ModelSerializer):
    """
       Serializer class for Mental Test Results for a given user
    """

    class Meta:
        model = MentalTestResult
        fields = ['url', 'test', 'user', 'test_field', 'value', 'current_user']

    current_user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    
    def to_representation(self, instance):
        instance['value'] = -1
        return instance


class MentalTestResultSerializer(serializers.ModelSerializer):
    """
        Serializer class for Mental Test Results
    """

    current_user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = MentalTestResult
        fields = ['url', 'test', 'user', 'test_field', 'value', 'current_user']
        depth = 2

    user = serializers.ReadOnlyField(source='user.username')



class MentalTestFieldSerializer(serializers.ModelSerializer):
    """
        Serializer class for Mental Test Field
    """

    field_type = MentalTestFieldTypeSerializer()
    current_user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = MentalTestField
        fields = ['id', 'test', 'name', 'description', 'field_type', 'weight', 'current_user']



class MentalTestSerializer(serializers.HyperlinkedModelSerializer):
    """
       Serializer class for Mental Test
    """
    
    mental_test_fields = MentalTestFieldSerializer(many=True, read_only=False)
    current_user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = MentalTest
        fields = ['url', 'id', 'owner', 'name', 'description', 'mental_test_fields', 'current_user']

    owner = serializers.ReadOnlyField(source='owner.username')


# Class for creating multiple results 
class MentalTestResultCreateSerializer(serializers.ModelSerializer):
    """
        Serializer class for Creating multiple Mental Test Results
        This class is needed for capturing all the Mental Test Results
        in one POST request.
    """

    class Meta:
        model = MentalTestResult
        fields = ['url', 'test', 'user', 'test_field', 'value']


    def create(self, validated_data):
        print("Creating mental test results: " + str(validated_data))
        MentalTestResult.objects.create(**validated_data)
 

