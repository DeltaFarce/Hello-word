from rest_framework import routers

from apps.debugtalks.views import DebugtalksViewSet

router = routers.DefaultRouter()
router.register('debugtalks', DebugtalksViewSet)
urlpatterns = [

]
urlpatterns += router.urls