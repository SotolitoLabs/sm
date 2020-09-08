from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .permissions import IsOwnerOrReadOnly
from .models import (MentalTest, MentalTestField, MentalTestFieldType,
                     MentalTestResult)
from .serializers import (UserSerializer, MentalTestSerializer,
                          MentalTestFieldSerializer, MentalTestFieldTypeSerializer,
                          MentalTestResultSerializer, MentalTestResultCreateSerializer)
from .renderers import PlainTextRenderer
from rest_framework.renderers import (BrowsableAPIRenderer, JSONRenderer, AdminRenderer,
                                     TemplateHTMLRenderer)

# Temporal imports
import sys


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(password=make_password(self.request.POST['password'], salt=None, hasher='default'))

    def perform_update(self, serializer):
        serializer.save(password=make_password(self.request.POST['password'], salt=None, hasher='default'))


class MentalTestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = MentalTest.objects.all().order_by('-id')
    serializer_class = MentalTestSerializer
    #renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    #renderer_classes = [JSONRenderer]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    #template_name = "test.html"

    #def get(self, request, pk):
    #    mt = get_object_or_404(MentalTest, pk=pk)
    #    serializer = MentalTestSerializer(mt)
    #    import logging
    #    logger = logging.getLogger(__name__)
    #    logger.info("USER: " + user)
    #    return Response({'serializer': serializer})

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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MentalTestResultsViewSet(viewsets.ModelViewSet):
    queryset = MentalTestResult.objects.all().order_by('-id')
    serializer_class = MentalTestResultSerializer
    user = ""


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

