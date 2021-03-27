from django.apps import AppConfig
import sys

class SherlockConfig(AppConfig):
    name = 'sherlock'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True

        # Uncomment the next two lines if you want a background process
        # constantly add network data to the database.
        from .jobs import jobs
        jobs.start()