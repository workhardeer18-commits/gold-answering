from django.core.management.base import BaseCommand

from UMS.models.user import User

SEED_USERNAME = "mahtab"
SEED_PASSWORD = "12345678"


class Command(BaseCommand):
    help = "Create or update the default Django admin superuser (idempotent)."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username=SEED_USERNAME,
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "is_admin": True,
            },
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.set_password(SEED_PASSWORD)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created admin user '{SEED_USERNAME}'."))
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Updated admin user '{SEED_USERNAME}' (password and flags refreshed).")
            )
