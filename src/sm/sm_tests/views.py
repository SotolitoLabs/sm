from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, permissions
from .permissions import IsOwnerOrReadOnly
from .models import (MentalTest, MentalTestField, MentalTestFieldType,
                     MentalTestResult)
from .serializers import (UserSerializer, MentalTestSerializer,
                          MentalTestFieldSerializer, MentalTestFieldTypeSerializer,
                          MentalTestResultSerializer)
from .renderers import PlainTextRenderer
from rest_framework.renderers import (BrowsableAPIRenderer, JSONRenderer, AdminRenderer,
                                     TemplateHTMLRenderer)

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



