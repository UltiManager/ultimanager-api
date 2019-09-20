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
    path("users/", views.UserCreateView.as_view(), name="user-create"),
]
