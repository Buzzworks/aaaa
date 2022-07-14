#!/usr/bin/env python
import os
import sys
import googlecloudprofiler
from django.conf import settings

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flexydial.settings')
    try:
        if settings.GS_BUCKET_NAME:
            googlecloudprofiler.start(
                service='flexydial-profiler',
                service_version='1.0.1',
                # verbose is the logging level. 0-error, 1-warning, 2-info,
                # 3-debug. It defaults to 0 (error) if not set.
                verbose=3,
                # project_id must be set if not running on GCP.
                # project_id='braided-hangout-356006',
            )
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
