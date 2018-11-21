from rest_framework import permissions



class UpdateOwnProfile(permissions.BasePermission):
    ''''Állow Users to edit thier own profile'''

    def has_object_permission(self, request, view, obj):
        ''''Check user is trying to edit their own profile'''

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

class PostOwnStatus(permissions.BasePermission):
    """"Allow users to update their own feed"""

    def has_object_permission(self, request, view, obj):
        """"Checks the user is trying to update their own status and not any other user's status """

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.username.id == request.user.id

