from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from sm_tests import views
from rest_framework.documentation import include_docs_urls

#from rest_framework.documentation import include_docs_urls
# COMMENTED FOR NOW, THIS HAS TO BE ENABLED from rest_framework_swagger.views import get_swagger_view



# Remember to run manage.py generateschema for static schema
#schema_view = get_swagger_view(title='adapp API')

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'mental_test', views.MentalTestViewSet)
router.register(r'mental_test_field', views.MentalTestFieldViewSet)
router.register(r'mental_test_field_type', views.MentalTestFieldTypeViewSet)
router.register(r'mental_test_result', views.MentalTestResultViewSet)
router.register(r'mental_test_results', views.MentalTestResultsViewSet, basename='MentalTestResult')
router.register(r'mental_test_diagnose', views.MentalTestDiagnosisViewSet, basename='MentalTestDiagnosis')
router.register(r'mental_test_diagnose_result', views.MentalTestDiagnosisResultsViewSet, basename='MentalTestDiagnosisResults')

urlpatterns = [
    path('api/admin/', admin.site.urls),
    re_path(r'^api/', include(router.urls)),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/docs/', include_docs_urls(title='Adapp API service'), name='api-docs'),
    #path(r'api/swagger', schema_view)
]

#urlpatterns = format_suffix_patterns(urlpatterns)
