from .views import ConfiguresViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('configures', ConfiguresViewSet)
urlpatterns = [

]
urlpatterns += router.urls
