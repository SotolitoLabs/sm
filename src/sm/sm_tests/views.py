from django.shortcuts import render
from django.contrib.auth.models import User
from .models import (MentalTest, MentalTestField, MentalTestFieldType,
    MentalTestResult)
from rest_framework import viewsets
from .serializers import  (UserSerializer, MentalTestSerializer,
        MentalTestFieldSerializer, MentalTestFieldTypeSerializer,
        MentalTestResultSerializer)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class MentalTestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = MentalTest.objects.all().order_by('-id')
    serializer_class = MentalTestSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MentalTestFieldViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = MentalTestField.objects.all().order_by('-id')
    serializer_class = MentalTestFieldSerializer

class MentalTestFieldTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = MentalTestFieldType.objects.all().order_by('-id')
    serializer_class = MentalTestFieldTypeSerializer

class MentalTestResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = MentalTestResult.objects.all().order_by('-id')
    serializer_class = MentalTestResultSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



