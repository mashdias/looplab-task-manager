from rest_framework import permissions

class IsAdminOrMemberTaskPermission(permissions.BasePermission):
    """
    Admin users can do anything.
    Member users can create tasks, and update only tasks assigned to them, cannot delete.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.user.role == 'Admin':
            return True
            
        # Members
        if view.basename == 'task':
            if request.method == 'DELETE':
                return False
            return True
            
        if view.basename == 'project':
            # Members can only view projects they own or are assigned tasks in (handled in get_queryset)
            if request.method in permissions.SAFE_METHODS:
                return True
            return False
            
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'Admin':
            return True
            
        # Member permissions on specific object
        if view.basename == 'task':
            if request.method in permissions.SAFE_METHODS:
                return obj.assigned_to == request.user or obj.project.owner == request.user
            if request.method in ['PUT', 'PATCH']:
                return obj.assigned_to == request.user
            if request.method == 'DELETE':
                return False
                
        if view.basename == 'project':
            if request.method in permissions.SAFE_METHODS:
                return True # get_queryset already filters
                
        return False
