from django.urls import path

from .api.views import (CreateUserView,
                        ConfirmUserView,
                        ResetPasswordView,
                        ConfirmPasswordResetView,
                        UpdateUserView,
                        ResetEmailView,
                        ConfirmEmailResetView)

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('create/confirm/', ConfirmUserView.as_view(), name='confirm_user'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password/confirm/', ConfirmPasswordResetView.as_view(), name='confirm_password_reset'),
    path('update/', UpdateUserView.as_view(), name='update_user'),
    path('reset_email/', ResetEmailView.as_view(), name='reset_email'),
    path('reset_email/confirm/', ConfirmEmailResetView.as_view(), name='confirm_email_reset')
]
