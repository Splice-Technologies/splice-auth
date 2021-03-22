from django.test import TestCase, RequestFactory

from .services import UserService
from .api.views import CreateUserView


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    # noinspection PyMethodMayBeStatic
    def test_user_creation(self):
        UserService.create_user('dimitar.popovski', 'email@gmail.com', 'password')
        UserService.create_user('minotaur.vampire', 'password', 'minotaur.vampire@splice.com')
        UserService.get_user_by_username('dimitar.popovski')

    def test_user_creation_view(self):
        request = self.factory.post('/api/users/create', data={
            'username': 'jovanovska.elena',
            'password': 'password',
        })
        response = CreateUserView.as_view()(request)

        self.assertEqual(response.status_code, 201)
