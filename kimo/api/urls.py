from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views
# from .views import UserViewSet
from .views import (
    UserDetailAPIView,
    UserListCreateAPIView,
    current_user,
    KidAPIViewSet,
    NotificationAPIViewSet,
    LocationAPIViewSet,
    RestrictionAPIViewSet
)

router = routers.SimpleRouter()
router.register('kid', KidAPIViewSet, base_name='kid')
router.register('notification', NotificationAPIViewSet, base_name='notification')
router.register('location', LocationAPIViewSet, base_name='location')
router.register('restriction', RestrictionAPIViewSet, base_name='restriction')
urlpatterns = router.urls
urlpatterns += [
    url('^user/$', UserListCreateAPIView.as_view(), name='account-list'),
    url('^user/current$', current_user, name='current-user'),
    url('^user/(?P<pk>[\d]+)/$', UserDetailAPIView.as_view(), name='account-detail'),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token-auth/', views.obtain_auth_token)
]
