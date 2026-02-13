"""Django management command to populate the OctoFit Tracker database."""

import os
import sys
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populate the OctoFit Tracker database with test data."

    def handle(self, *args, **options):
        # Ensure backend directory is on sys.path so populate_db can be imported.
        backend_dir = settings.BASE_DIR
        if str(backend_dir) not in sys.path:
            sys.path.append(str(backend_dir))

        try:
            import populate_db
        except Exception as exc:
            raise RuntimeError("Unable to import populate_db.py") from exc

        # Reuse the script's main entry point.
        if hasattr(populate_db, "main"):
            populate_db.main()
        else:
            raise RuntimeError("populate_db.py does not define a main() function")
