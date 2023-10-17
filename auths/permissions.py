from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class RoleBasedPermission(BasePermission):
    role = 0

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user.is_authenticated:
            return False

        return request.user.role == self.role


class IsSuperAdmin(RoleBasedPermission):
    role = 1
