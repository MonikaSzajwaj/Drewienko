from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.dispatch import receiver
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, FormView, DetailView, TemplateView, UpdateView
from .forms import SignUpForm, UserEditForm, UserProfileEditForm
from .models import User, UserProfile


class UserProfileView(DetailView):
    model = UserProfile
    template_name = "portal_v1/user_profile.html"
    context_object_name = "profile"



class ChangePassword(FormView, LoginRequiredMixin):
    template_name = "portal_v1/password_change.html"
    form_class = PasswordChangeForm

    def get_form(self):
        if self.request.POST:
            return self.form_class(self.request.user, self.request.POST)
        return self.form_class(self.request.user)

    def form_valid(self, form):
        messages.success(request=self.request, message="Hasło zmienione prawidłowo")
        form.save()
        return redirect(reverse('login'))

    def get_success_url(self) -> str:
        return reverse("profile")

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Użytkownik zarejestrowany. Możesz się zalogować')
            return redirect('login')
    else:
        form = SignUpForm()
    return render (request, 'portal_v1/register.html', {'form': form})



class LoginView(View):
    template_name = "portal_v1/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("announcement-home")
        return render(request, self.template_name, {})

    def post(self, request):
        username: str = request.POST.get("username")
        password: str = request.POST.get("password")

        user: User or None = authenticate(username=username,
                                          password=password)

        if user:
            login(request, user)
            return redirect("announcement-home")

        messages.error(request, "Zła nazwa użytkownika lub hasło")
        return redirect("login")


def logout_view(request):
    logout(request)
    return redirect("announcement-home")


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, 'Wylogowano pomyślnie')


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, 'Zalogowano pomyślnie')


@login_required
def profile(request):
    UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        u_form = UserEditForm(request.POST, instance=request.user)
        p_form = UserProfileEditForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Twoje konto zostało zaktualizowane')
            return redirect('profile')

    else:
        u_form = UserEditForm(instance=request.user)
        p_form = UserProfileEditForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'portal_v1/user_profile.html', context)