from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required
from ..forms import SignUpForm, StyledAuthenticationForm

def account(request):
    action = request.POST.get("action", request.GET.get("action", "login"))
    next_url = request.GET.get("next", request.POST.get("next", "/"))
    if not url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
        next_url = "/"

    if request.user.is_authenticated:
        return redirect(next_url)

    if action == "signup":
        form = SignUpForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
        login_form = StyledAuthenticationForm()
    else:
        login_form = StyledAuthenticationForm(request, request.POST or None)
        form = SignUpForm()
        if request.method == "POST" and login_form.is_valid():
            login(request, login_form.get_user())
            return redirect(next_url)

    return render(
        request,
        "account.html",
        {"login_form": login_form, "signup_form": form, "action": action, "next": next_url},
    )

@login_required
def account_logout(request):
    if request.method == "POST":
        logout(request)
    return redirect("home")