import os
import django
from django.conf import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "app.settings"


def pytest_configure():
    settings.DEBUG = False
    django.setup()
