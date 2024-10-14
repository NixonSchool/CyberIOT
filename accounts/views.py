# views.py
# Defines custom views for user signup, login, logout, and password reset functionality.
# Extends default Django authentication views and adds custom form handling and success redirects.
# Views do the heavy lifting in Django. They act as the glue between forms, models, and templates,
# managing the logic and data flow and helping in generating responses and handling URLs.

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import PasswordResetRequestForm

User = get_user_model()

# -------------- Sign up stuff----------------------
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return str(self.success_url)


# -----------------Login Stuff-----------------------
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('mainpage:main_page')

# ------- Handles user logout: Overrides `get` method to log out the user and redirect to the login page -------
class CustomLogoutView(CreateView):

    # --------- Handles GET requests for user logout --------------
    # --------- Uses the `logout` function from `django.contrib.auth` to clear the user's session -----------
    # --------- After logging out, the user is redirected to the 'logout.html' template for confirmation ---------
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, 'registration/logout.html')


class PasswordResetRequestView(View):
    template_name = 'registration/password_reset_request.html'
    form_class = PasswordResetRequestForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data.get('username')  # Optional

            # Check if user exists with given email (and username if provided)
            user_query = User.objects.filter(email=email)
            if username:
                user_query = user_query.filter(username=username)

            if user_query.exists():
                # "Fake" send email
                messages.success(request, "A password reset link has been sent to your email.")
                return redirect('accounts:password_reset_done')
            else:
                messages.error(request, "No account found with the provided information.")

        return render(request, self.template_name, {'form': form})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'