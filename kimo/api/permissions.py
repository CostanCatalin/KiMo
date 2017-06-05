from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "You do not own this resource."

    def has_object_permission(self, request, view, obj):
        return obj.parent == request.user


class IsMyKid(BasePermission):
    message = "This is not for you to see"

    def has_object_permission(self, request, view, obj):
        return obj.kid.parent == request.user


class IsSelf(BasePermission):
    message = "You do not belong here."

    def has_object_permission(self, request, view, obj):
        return obj == request.user
