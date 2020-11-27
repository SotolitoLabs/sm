from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .permissions import (IsOwnerOrReadOnly, IsHRAdmin, 
        IsOwner)

from .models import (MentalTest, MentalTestField, MentalTestFieldType,
        MentalTestResult)

from .serializers import (UserSerializer, MentalTestSerializer,
        MentalTestFieldSerializer, MentalTestFieldTypeSerializer,
        MentalTestResultSerializer, MentalTestResultCreateSerializer)

from rest_framework.renderers import (BrowsableAPIRenderer, JSONRenderer, AdminRenderer,
        TemplateHTMLRenderer)


from rest_framework.request import Request

# Temporal imports
import sys


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [IsOwner | permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(password=make_password(self.request.POST['password'], salt=None, hasher='default'))

    def perform_update(self, serializer):
        serializer.save(password=make_password(self.request.POST['password'], salt=None, hasher='default'))


class MentalTestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = MentalTest.objects.all().order_by('id')
    serializer_class = MentalTestSerializer
    permission_classes = [permissions.IsAuthenticated | IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MentalTestFieldViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = MentalTestField.objects.all().order_by('-id')
    serializer_class = MentalTestFieldSerializer
    permission_classes = [permissions.IsAuthenticated]

class MentalTestFieldTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = MentalTestFieldType.objects.all().order_by('-id')
    serializer_class = MentalTestFieldTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class MentalTestResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = MentalTestResult.objects.all().order_by('-id')
    serializer_class = MentalTestResultSerializer
    #permission_classes = [permissions.IsAuthenticated | IsHRAdmin]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MentalTestResultsViewSet(viewsets.ModelViewSet):
    queryset = MentalTestResult.objects.all().order_by('-id')
    serializer_class = MentalTestResultSerializer
    #permission_classes = [permissions.IsAuthenticated & (IsHRAdmin | IsOwner)]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "test"
    user = ""

    def retrieve(self, request, *args, **kwargs):
        queryset = MentalTestResult.objects.filter(user = self.request.user.id, test = kwargs['test']).order_by('id')
        if len(queryset) > 0:
            serializer = MentalTestResultSerializer(queryset, many=True, context={'request': request})
        else:
            queryset = MentalTestField.objects.filter(test = kwargs['test']).order_by('id')
            serializer = MentalTestFieldSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        instance = None
        return_message = {"failed": "Failed to create Mental Test Result"}
        return_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        write_serializer = MentalTestResultCreateSerializer(data=request.data, many=True, context={'request': request})
        write_serializer.is_valid(raise_exception=True)

        try:
            self.perform_update(write_serializer)
            return_message = {"success": "Mental Test Result Succesfully Updated"}
            return_status = status.HTTP_200_OK
        except:
            instance = self.perform_create(write_serializer)
            return_message = {"success": "Mental Test Result Succesfully Created"}
            return_status = status.HTTP_201_CREATED

        return Response(return_message, return_status)


    def perform_create(self, serializer):
        return serializer.save()


    def perform_update(self, serializer):
        for d in serializer.validated_data:
            m = MentalTestResult.objects.get(test = d['test'], user = d['user'], test_field = d['test_field'] )
            if not isinstance(m, list):
                m.value = d['value']
                m.save()
            else:
                raise Exception("Multiple response values")

