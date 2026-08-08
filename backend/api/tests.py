from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Project, Task, ActivityLog

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.member_user = User.objects.create_user(username='member', password='password', role='Member')
        
        self.project = Project.objects.create(name='Test Project', owner=self.admin_user)
        self.task = Task.objects.create(
            title='Test Task', 
            project=self.project, 
            assigned_to=self.member_user
        )

    def get_token(self, username, password):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': username, 'password': password})
        return response.data['access']

    def test_login_jwt(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'admin', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_member_cannot_delete_task(self):
        token = self.get_token('member', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_task(self):
        token = self.get_token('admin', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_task_soft_delete(self):
        token = self.get_token('admin', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        
        url = reverse('task-detail', args=[self.task.id])
        self.client.delete(url)
        
        # Verify it's still in DB but is_deleted=True
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_deleted)
        
        # Verify it's not in the regular queryset anymore
        response = self.client.get(reverse('task-list'))
        self.assertEqual(len(response.data['results']), 0)

    def test_activity_log_creation(self):
        initial_count = ActivityLog.objects.count()
        
        # Create a project as admin to trigger signal
        token = self.get_token('admin', 'password')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        
        url = reverse('project-list')
        self.client.post(url, {'name': 'New Project', 'description': 'desc'})
        
        self.assertEqual(ActivityLog.objects.count(), initial_count + 1)
        log = ActivityLog.objects.latest('timestamp')
        self.assertEqual(log.action, 'CREATE')
        self.assertEqual(log.model_name, 'Project')
