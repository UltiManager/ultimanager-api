from django.urls import path

from account.api import views


app_name = "account:api"


urlpatterns = [
    path(
        "email-verification-requests/",
        views.EmailVerificationRequestView.as_view(),
        name="email-verification-request-create",
    ),
    path(
        "email-verifications/",
        views.EmailVerificationView.as_view(),
        name="email-verification-create",
    ),
    path(
        "password-reset-requests/",
        views.PasswordResetRequestView.as_view(),
        name="password-reset-request-create",
    ),
    path(
        "password-resets/",
        views.PasswordResetView.as_view(),
        name="password-reset-create",
    ),
    path("users/", views.UserCreateView.as_view(), name="user-create"),
]
