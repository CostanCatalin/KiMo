from authentication.models import Account
from kids.models import Kid, Location, Notification, Encounter, Restriction
from django.db.models import Q

from .serialisers import (
    UserCreateSerializer,
    UserDetailSerializer,
    KidSerializer,
    NotificationSerializer,
    LocationSerializer,
    RestrictionSerializer
)

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.decorators import detail_route, list_route
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwner, IsSelf, IsMyKid


class UserListCreateAPIView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsSelf]


class KidAPIViewSet(ModelViewSet):
    serializer_class = KidSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Kid.objects.filter(parent=self.request.user)

    @detail_route(['GET'], permission_classes=[IsAuthenticated, IsMyKid])
    def notification(self, request, pk):
        queryset = Notification.objects.filter(kid_id=pk)
        serializer = NotificationSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)


class NotificationAPIViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsMyKid]

    def get_queryset(self, *args, **kwargs):
        queryset = Notification.objects.filter(kid__parent=self.request.user).order_by('-date_created')
        query = self.request.GET.get('kid')
        if query:
            queryset = queryset.filter(
                Q(kid=query)
            )
        return queryset


class LocationAPIViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsMyKid]

    def get_queryset(self, *args, **kwargs):
        queryset = Location.objects.filter(kid__parent=self.request.user).order_by('-date_created')
        kid = self.request.GET.get('kid')
        limit = self.request.GET.get('limit')
        if type(limit) is not int:
            try:
                limit = int(limit)
            except ValueError:
                limit = None
            except TypeError:
                pass

        if kid:
            queryset = queryset.filter(
                Q(kid=kid)
            )
        if limit:

            queryset = queryset[:limit]
        return queryset


class RestrictionAPIViewSet(ModelViewSet):
    serializer_class = RestrictionSerializer
    permission_classes = [IsAuthenticated, IsMyKid]

    def get_queryset(self, *args, **kwargs):
        queryset = Restriction.objects.filter(kid__parent=self.request.user).order_by('-date_created')
        kid = self.request.GET.get('kid')
        limit = self.request.GET.get('limit')
        if type(limit) is not int:
            try:
                limit = int(limit)
            except ValueError:
                limit = None
            except TypeError:
                pass

        if kid:
            queryset = queryset.filter(
                Q(kid=kid)
            )
        if limit:
            queryset = queryset[:limit]
        return queryset









