from django.views.generic import TemplateView

from .services import UserService


class ConfirmUserTemplateView(TemplateView):
    template_name = 'users/confirmed_user.html'

    def get_context_data(self, **kwargs):
        confirmation_code = self.request.GET.get('confirmation_code', '')
        confirmation = UserService.confirm_user(confirmation_code)

        return {'success': confirmation, 'username': 'my friend'}
