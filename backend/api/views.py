from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Project, Task, ActivityLog
from .serializers import ProjectSerializer, TaskSerializer, ActivityLogSerializer
from .permissions import IsAdminOrMemberTaskPermission

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrMemberTaskPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Project.objects.all()
        # Members see projects they own or where they are assigned tasks
        return Project.objects.filter(
            Q(owner=user) | Q(tasks__assigned_to=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrMemberTaskPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'project']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(is_deleted=False)
        
        if user.role == 'Admin':
            return queryset
            
        # Members see tasks they are assigned to, or tasks in projects they own
        return queryset.filter(
            Q(assigned_to=user) | Q(project__owner=user)
        ).distinct()

    def destroy(self, request, *args, **kwargs):
        # Soft delete
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdminOrMemberTaskPermission]
    
    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return ActivityLog.objects.all().order_by('-timestamp')
        return ActivityLog.objects.filter(user=self.request.user).order_by('-timestamp')
