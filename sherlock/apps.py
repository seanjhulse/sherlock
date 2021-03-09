from django.apps import AppConfig
import sys

class SherlockConfig(AppConfig):
    name = 'sherlock'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True

        from .jobs import jobs
        jobs.start()