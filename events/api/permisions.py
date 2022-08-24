# permissions.py

from rest_framework import permissions
from api.models import User

class OnlyBussiness(permissions.BasePermission):

    restricted_methods = ["PUT", "PATCH", "POST", "DELETE"]

    def has_permission(self, request, view):
        
        if request.method in self.restricted_methods:

            if not request.user.is_authenticated:
                return False

            if not request.user.is_superuser:            

                user = User.objects.filter(id=request.user.id).first()

                if user.type not in "BU":
                    return False

        return True