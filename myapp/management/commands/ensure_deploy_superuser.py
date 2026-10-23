import os

from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create the initial deployment administrator from environment variables.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not email or not password:
            raise CommandError(
                'Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and '
                'DJANGO_SUPERUSER_PASSWORD in the service environment.'
            )

        User = get_user_model()
        lookup = {User.USERNAME_FIELD: username}

        try:
            user = User._default_manager.get(**lookup)
        except User.DoesNotExist:
            try:
                password_validation.validate_password(password)
            except ValidationError as exc:
                raise CommandError('; '.join(exc.messages)) from exc

            User._default_manager.db_manager().create_superuser(
                **lookup,
                email=email,
                password=password,
            )
            self.stdout.write(self.style.SUCCESS('Deployment administrator created.'))
            return

        if not user.is_superuser:
            raise CommandError(
                'The configured username already exists and is not a superuser.'
            )

        self.stdout.write('Deployment administrator already exists; leaving unchanged.')
