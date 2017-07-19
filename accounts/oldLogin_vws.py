################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Accounts View.                                               ##
################################################################################



################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.shortcuts import render, redirect


################################################################################
## Import Third Party Models.                                                 ##
################################################################################


################################################################################
## Import Defined Models.                                                     ##
################################################################################
from .forms import UserLoginForm, UserRegisterForm





################################################################################
## Define the Accounts Login.                                                 ##
################################################################################
def login_view(request):
    print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")

    return render(request, "form.html", {"form":form, "title": title})






################################################################################
## Define the Accounts Registration.                                          ##
################################################################################
def register_view(request):
    print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }

    return render(request, "form.html", context)





################################################################################
## Define the Accounts Logout.                                                ##
################################################################################
def logout_view(request):
    logout(request)
    return redirect("/")
