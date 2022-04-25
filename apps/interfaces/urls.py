from rest_framework import routers

from apps.interfaces.views import InterfacesViewSet

router = routers.DefaultRouter()
router.register('interfaces', InterfacesViewSet)
urlpatterns = [

]
urlpatterns += router.urls