from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .permissions import (IsOwnerOrReadOnly, IsHRAdmin, 
        IsOwner)

from .models import (MentalTest, MentalTestField, MentalTestFieldType,
        MentalTestResult, MentalTestDiagnosis)

from .serializers import (UserSerializer, MentalTestSerializer,
        MentalTestFieldSerializer, MentalTestFieldTypeSerializer,
        MentalTestResultSerializer, MentalTestResultCreateSerializer,
        MentalTestDiagnosisSerializer)

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


class MentalTestDiagnosisViewSet(viewsets.ModelViewSet):
    queryset = MentalTestDiagnosis.objects.all().order_by('-id')
    serializer_class = MentalTestResultSerializer
    #permission_classes = [permissions.IsAuthenticated & (IsHRAdmin | IsOwner)]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "test"
    user = ""

    def retrieve(self, request, *args, **kwargs):
        results_sum = 0
        max_diagnose_value = 0
        queryset = MentalTestResult.objects.filter(user = self.request.user.id, test = kwargs['test']).order_by('id')
        # TODO optimize this
        total_results = len(queryset)
        if total_results > 0:
            for result in queryset:
                max_diagnose_value += result.test_field.field_type.final_range
                results_sum += int(result.value)
            res = '{"test_id": %s, "diagnosed_value": %s, "max_diagnose_value": %s}' % (kwargs['test'], results_sum, max_diagnose_value)
        else:
            res = '{"Error": No result for test: %s}' % (kwargs['test'])
        return Response(res)

class MentalTestDiagnosisResultsViewSet(viewsets.ModelViewSet):
    queryset = MentalTestDiagnosis.objects.all().order_by('-id')
    serializer_class = MentalTestDiagnosisSerializer
    #permission_classes = [permissions.IsAuthenticated & (IsHRAdmin | IsOwner)]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "test"
    user = ""

    def retrieve(self, request, *args, **kwargs):
        print("DEBUG:: en retrieve USER: " + str(self.request.user))
        print("DEBUG:: en retrieve TEST: " + kwargs['test'])

        results_sum = 0
        max_diagnose_value = 0
        queryset = MentalTestDiagnosis.objects.filter(user = self.request.user.id, test = kwargs['test']).order_by('id')
        # TODO optimize this
        total_results = len(queryset)
        print("DEBUG:: en retrieve RESULTS: " + str(total_results))
        serializer = MentalTestDiagnosisSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        instance = None
        return_message = {"failed": "Failed to create Mental Test Result"}
        return_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        max_diagnose_value = 0
        results_sum = 0

        print("DEBUG:: en Create USER: " + str(self.request.user))
        print("DEBUG:: en retrieve TEST: " + str(self.request.data['test']))
        queryset = MentalTestResult.objects.filter(user = self.request.user.id, test = self.request.data['test']).order_by('id')
        print("DEBUG:: en Create queryset: " + str(queryset))
        # TODO optimize this
        total_results = len(queryset)
        if total_results > 0:
            for result in queryset:
                max_diagnose_value += result.test_field.field_type.final_range
                results_sum += int(result.value)

            md = None
            try:
                md = MentalTestDiagnosis.objects.filter(user = self.request.user.id, test = self.request.data['test']).order_by('id')
                md[0].value = results_sum
                md[0].max_value = max_diagnose_value
                md[0].save()
                return_message = {"success": "Mental Test Diagnosis Succesfully Updated"}
                return_status = status.HTTP_200_OK
            except:
                mt = MentalTest.objects.get(id=self.request.data['test'])
                md = MentalTestDiagnosis(test = mt, user = self.request.user, value = results_sum, max_value = max_diagnose_value)
                return_message = {"success": "Mental Test Diagnosis Succesfully Created"}
                return_status = status.HTTP_201_CREATED
                md.save()
        #write_serializer = MentalTestDiagnosisCreateSerializer(data=md, many=True, context={'request': request})
        #write_serializer.is_valid(raise_exception=True)

        #try:
        #    self.perform_update(write_serializer)
        #    return_message = {"success": "Mental Test Result Succesfully Updated"}
        #    return_status = status.HTTP_200_OK
        #except:
        #    instance = self.perform_create(write_serializer)
        #    return_message = {"success": "Mental Test Result Succesfully Created"}
        #    return_status = status.HTTP_201_CREATED

        return Response(return_message, return_status)





