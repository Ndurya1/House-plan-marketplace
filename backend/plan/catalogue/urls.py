from rest_framework.routers import DefaultRouter
from .views import CatalogueViewSet

router = DefaultRouter()
router.register (r'catalogue', CatalogueViewSet)
urlpatterns = router.urls