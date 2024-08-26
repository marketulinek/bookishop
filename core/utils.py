from django.conf import settings


def debug_print(message):
    if settings.DEBUG:
        print(message)
