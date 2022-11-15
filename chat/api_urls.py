from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('', views.ChatViewSets)
router.register('room/data', views.RoomViewSets)

urlpatterns = router.urls 