from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase

class PublicPagesTests(SimpleTestCase):
    def test_homepage_links_to_admin(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ir al panel de administración')

    def test_health_check(self):
        response = self.client.get('/health/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'ok')


class EnsureDeploySuperuserTests(TestCase):
    def test_creates_superuser_and_leaves_it_unchanged(self):
        environment = {
            'DJANGO_SUPERUSER_USERNAME': 'site-admin',
            'DJANGO_SUPERUSER_EMAIL': 'admin@example.com',
            'DJANGO_SUPERUSER_PASSWORD': 'xX9!vQ2#pL8@kR5$mN4',
        }
        with patch.dict('os.environ', environment):
            call_command('ensure_deploy_superuser', verbosity=0)
            user = get_user_model().objects.get(username='site-admin')

            self.assertTrue(user.is_staff)
            self.assertTrue(user.is_superuser)
            self.assertTrue(user.check_password(environment['DJANGO_SUPERUSER_PASSWORD']))

            call_command('ensure_deploy_superuser', verbosity=0)
            self.assertEqual(get_user_model().objects.count(), 1)
