from django.contrib.auth.models import User
from .models import (MentalTest, MentalTestField, MentalTestFieldType,
    MentalTestResult)
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class MentalTestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MentalTest
        fields = ['owner', 'name', 'description']

    owner = serializers.ReadOnlyField(source='owner.username')

class MentalTestFieldTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MentalTestFieldType
        fields = ['name', 'description']

class MentalTestFieldSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MentalTestField
        fields = ['test', 'name', 'description', 'field_type', 'weight']

class MentalTestResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MentalTestResult
        fields = ['test', 'user', 'test_field', 'value']

    user = serializers.ReadOnlyField(source='user.username')
