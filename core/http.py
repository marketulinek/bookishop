import json

from core.utils import debug_print
from django.http import HttpResponse


class HttpToastResponse:
    """
    A class to generate an HttpResponse with a toast notification for use in HTMX requests.

    This class helps in creating a standardized HttpResponse that includes a trigger for
    a toast notification, which can be used to display success or error messages to users
    via HTMX. The toast notification is triggered using the 'HX-Trigger' header.
    """

    def __init__(self, status_code, message, level=None):
        self.status_code = status_code
        self.message = message
        self.level = self._validate_level(level) or self._set_level()

    def _set_level(self):
        if self.status_code >= 400:
            return 'danger'
        return 'success'

    def _validate_level(self, level):
        levels = ('info', 'success', 'warning', 'danger')
        if level not in levels:
            debug_print(f"Warning: Invalid level '{level}' provided. Defaulting to '{self._set_level()}'")
            return None
        return level

    def get_response(self):
        return HttpResponse(
            status=self.status_code,
            headers={'HX-Trigger': json.dumps({
                'showMessage': {'level': self.level, 'message': self.message}
            })}
        )
