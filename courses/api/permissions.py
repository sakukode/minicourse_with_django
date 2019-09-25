from rest_framework import permissions

class CoursePermission(permissions.DjangoModelPermissionsOrAnonReadOnly):
    """
    Object-level permission to only allow owners of an object to edit it
    """

    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed to any request,
        so we'll always allow GET, HEAD or OPTIONS requests
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named 'owner
        return obj.author == request.user
