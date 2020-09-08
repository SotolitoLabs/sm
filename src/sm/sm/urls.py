from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from sm_tests import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'mental_test', views.MentalTestViewSet)
router.register(r'mental_test_field', views.MentalTestFieldViewSet)
router.register(r'mental_test_field_type', views.MentalTestFieldTypeViewSet)
router.register(r'mental_test_result', views.MentalTestResultViewSet)
router.register(r'mental_test_results', views.MentalTestResultsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

#urlpatterns = format_suffix_patterns(urlpatterns)
