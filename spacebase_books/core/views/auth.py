from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from ..forms import SignUpForm


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("books:dashboard")
    else:
        form = SignUpForm()
    return render(request, "registration/register.html", {"form": form})
