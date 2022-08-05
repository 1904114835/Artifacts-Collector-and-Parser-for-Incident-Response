from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


def environment(**options):
   from main.views import type_of_artifacts
   env = Environment(**options)
   env.globals.update({
      'static': staticfiles_storage.url,
      'url': reverse,
      'len': len,
      'type_of_artifacts': type_of_artifacts,
      'str': str
   })
   return env
