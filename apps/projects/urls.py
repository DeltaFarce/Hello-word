from rest_framework import routers

from apps.projects.views import ProjectsViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectsViewSet)
urlpatterns = [

]
urlpatterns += router.urls