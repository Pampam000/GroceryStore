from rest_framework import permissions as p


class IsAdminOrReadOnly(p.BasePermission):
    def has_permission(self, request, view):
        return request.method in p.SAFE_METHODS or \
            bool(request.user and request.user.is_staff)

