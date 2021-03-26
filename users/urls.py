from django.urls import path

from .api.views import (CreateUserView,
                        ConfirmUserView,
                        ResetPasswordView,
                        ConfirmPasswordResetView,
                        UpdateUserView)

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('create/confirm/', ConfirmUserView.as_view(), name='confirm_user'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password/confirm/', ConfirmPasswordResetView.as_view(), name='confirm_reset_password'),
    path('update/', UpdateUserView.as_view(), name='update_user'),
]
