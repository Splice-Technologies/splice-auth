from django.urls import path

from .api.views import CreateUserView, ConfirmUserView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('create/confirm/', ConfirmUserView.as_view(), name='confirm_user'),
]
