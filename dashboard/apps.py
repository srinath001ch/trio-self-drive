import os

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"

    def ready(self):
        try:
            from django.contrib.auth import get_user_model

            User = get_user_model()

            username = os.environ.get("ADMIN_USERNAME")
            email = os.environ.get("ADMIN_EMAIL")
            password = os.environ.get("ADMIN_PASSWORD")

            if not username or not password:
                return

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                )
                print("Superuser created successfully.")

        except Exception:
            # Ignore errors during startup (e.g. before migrations)
            pass
