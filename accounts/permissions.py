from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserCanWriteOrReadOnly(BasePermission):

    message = {
        'permission': 'you are not the owner of this account please choose your account.'
    }

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif hasattr(obj, 'user'):
            return request.user == obj.user
        else:
            return request.user == obj.account.user



