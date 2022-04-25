from rest_framework import routers

from apps.testsuits.views import TestSuitViewSet

router = routers.DefaultRouter()
router.register('testsuits', TestSuitViewSet)
urlpatterns = [

]
urlpatterns += router.urls