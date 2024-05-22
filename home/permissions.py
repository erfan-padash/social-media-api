from rest_framework.permissions import BasePermission, SAFE_METHODS


class WriteOrReadOnly(BasePermission):

    message = {
        'permission': 'you are not the owner of this object.'
    }

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user == obj.account.user
