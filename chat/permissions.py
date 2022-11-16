from rest_framework import permissions

class RoomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in ['POST','PUT','DELETE']:
            return True 
        return request.user.is_authenticated