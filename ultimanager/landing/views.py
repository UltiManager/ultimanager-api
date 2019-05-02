from django.views import generic


class LandingView(generic.TemplateView):
    """
    Show a landing page for the application.
    """

    template_name = "landing/landing.html"
