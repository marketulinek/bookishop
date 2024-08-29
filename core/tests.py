import json

from io import StringIO
from django.core.management import call_command
from django.http import HttpResponse
from django.test import SimpleTestCase, TestCase

from .http import HttpToastResponse


class PendingMigrationsTests(TestCase):

    def test_no_pending_migrations(self):
        out = StringIO()
        try:
            call_command(
                'makemigrations',
                '--check',
                stdout=out,
                stderr=StringIO(),
            )
        except SystemExit:
            raise AssertionError(f"Pending migrations:\n{out.getvalue()}") from None


class HttpToastResponseTests(SimpleTestCase):

    def test_success_response(self):
        response = HttpToastResponse(200, 'Successful Request').get_response()
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['HX-Trigger'], json.dumps({
            'showMessage': {'level': 'success', 'message': 'Successful Request'}
        }))

    def test_error_response(self):
        response = HttpToastResponse(400, 'Bad Request').get_response()
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['HX-Trigger'], json.dumps({
            'showMessage': {'level': 'danger', 'message': 'Bad Request'}
        }))

    def test_custom_level(self):
        response = HttpToastResponse(200, 'Info Message', 'info').get_response()
        self.assertEqual(response.headers['HX-Trigger'], json.dumps({
            'showMessage': {'level': 'info', 'message': 'Info Message'}
        }))

    def test_invalid_level_defaults(self):
        response = HttpToastResponse(200, 'Message', 'invalid-level').get_response()
        self.assertEqual(response.headers['HX-Trigger'], json.dumps({
            'showMessage': {'level': 'success', 'message': 'Message'}
        }))

    def test_invalid_level_for_error(self):
        response = HttpToastResponse(500, 'Error Message', 'invalid-level').get_response()
        self.assertEqual(response.headers['HX-Trigger'], json.dumps({
            'showMessage': {'level': 'danger', 'message': 'Error Message'}
        }))
