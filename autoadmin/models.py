from django.conf import settings

from autoadmin import autoadmin, autodatabrowse

for app in getattr(settings, 'AUTOADMIN_APPS', []):
    autoadmin(app)

for app in getattr(settings, 'AUTOADMIN_BROWSER_APPS', []):
    autodatabrowse(app)
