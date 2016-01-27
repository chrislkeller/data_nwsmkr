"""
WSGI config for data_nwsmkr project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ["CONFIG_PATH"] = "%s_PRODUCTION" % ("data_nwsmkr".upper())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_nwsmkr.settings_production")

application = get_wsgi_application()
