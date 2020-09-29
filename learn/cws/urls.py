from rest_framework import routers
from cws.views import *
router = routers.SimpleRouter()

router.register('category',CategoryViewset)
router.register('course',CourseViewset)
router.register('order',OrderViewset)


urlpatterns = router.urls



