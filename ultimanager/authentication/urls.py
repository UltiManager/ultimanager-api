from django.urls import path

from authentication import views

app_name = "authentication"

urlpatterns = [
    path(
        "sessions/", views.SessionCreationView.as_view(), name="session-create"
    )
]
