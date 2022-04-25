from rest_framework import routers

from apps.reports.views import ReportsViewSet

router = routers.DefaultRouter()
router.register('reports', ReportsViewSet)
urlpatterns = [

]
urlpatterns += router.urls