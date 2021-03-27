from django.test import TestCase

from .utils import UsersUtils


class UserTestCase(TestCase):
    def test_message_response_generator(self):
        response = UsersUtils.generate_message_response('Testing message', success=True)
        print(response.data['success'])
