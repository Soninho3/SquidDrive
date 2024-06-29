from django.shortcuts import render
from django.views import View


class HomeView(View):
    """
    Displays the home page.
    """

    def get(self, request):
        return render(request, "home.html")
