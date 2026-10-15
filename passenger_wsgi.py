"""
Entry point for cPanel / Phusion Passenger.

Point the new domain's Python application at this file and set the
callable name to ``application``. Do not put this project inside the
other site's document root.
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_cv.settings')

from website_cv.wsgi import application  # noqa: E402
