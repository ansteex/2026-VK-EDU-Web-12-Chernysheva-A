from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm
def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')
    form = LoginForm(request=request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())

        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)

        return redirect('questions:index')

    return render(request, 'core/login.html', {
        'form': form,
        'next': next_url,
    })

def signup(request):
    return render(request, 'core/signup.html')


def profile(request):
    return render(request, 'core/profile.html')
