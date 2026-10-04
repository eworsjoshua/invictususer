from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import profile


class UserDashboardTests(APITestCase):
	def setUp(self):
		self.password = 'test-password-123'
		self.user = User.objects.create_user(
			username='dashboard-test-user',
			email='dashboard-test@example.com',
			password=self.password,
		)
		profile.objects.create(
			user=self.user,
			fullname='Dashboard Test User',
			username=self.user.username,
			phone='555-0100',
			email=self.user.email,
			gender='male',
		)

	def test_dashboard_requires_authentication(self):
		response = self.client.get('/api/dashboard/')

		self.assertIn(response.status_code, (401, 403))

	def test_login_session_can_load_dashboard(self):
		login_response = self.client.post(
			'/api/login/',
			{'username': self.user.username, 'password': self.password},
			format='json',
		)
		dashboard_response = self.client.get('/api/dashboard/')

		self.assertEqual(login_response.status_code, 200)
		self.assertEqual(dashboard_response.status_code, 200)
		self.assertEqual(dashboard_response.data['username'], self.user.username)
