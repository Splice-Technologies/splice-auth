from django.views.generic import TemplateView

from .services import UsersService


class ConfirmUserTemplateView(TemplateView):
    template_name = 'users/public/user_confirmed.html'

    def get_context_data(self, **kwargs) -> dict:
        confirmation_code = self.request.GET.get('confirmation_code', '')
        confirmation = UsersService.confirm_user(confirmation_code)

        return {'success': confirmation, 'username': 'my friend'}
