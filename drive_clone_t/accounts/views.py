from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from accounts.forms import UserRegistrationForm

from drive_clone_t.utils import get_errors, add_error
# Create your views here.


class LoginView(View):
    def get(self, request):
        errors = get_errors(
            request=request,
            url_name='Login',
        )
        
        return render(request, "authentication/login.html", {"errors": errors})
    
    def post(self, request):
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            add_error(
                message="Please fill in all the fields",
                request=request,
                tag="login_error",
                url_name="login",
            )
            return redirect("login")
        
        user = authenticate(request, username=username, password=password)
        
        if not user:
            add_error(
                message="Invalid username or password",
                request=request,
                tag="login_error",
                url_name="login",
            )
            return redirect("login")
        
        login(request, user)
        return redirect('home')
    
    
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "authentication/logout.html")
     
    def post(self, request):
        logout(request)
        return redirect("login")
    
    
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username} !')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form}) 