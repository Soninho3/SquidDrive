from django.urls import path
from accounts.views import LoginView, LogoutView
from accounts.views import register


urlpatterns = [
   path('login', LoginView.as_view(), name="login"),
   path('register', register, name="register"),
   path('logout', LogoutView.as_view(), name="logout"), 
]

