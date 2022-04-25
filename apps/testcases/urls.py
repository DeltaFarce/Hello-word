from rest_framework import routers

from apps.testcases.views import TestCaseViewSet

router = routers.DefaultRouter()
router.register('testcases', TestCaseViewSet)
urlpatterns = [

]
urlpatterns += router.urls