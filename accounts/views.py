from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import RegisterForm, ProfileForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            ):
                return redirect(next_url)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Nieprawidlowa nazwa uzytkownika lub haslo',
                'next': next_url
            })
    return render(request, 'accounts/login.html', {'next': next_url})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
