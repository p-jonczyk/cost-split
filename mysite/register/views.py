from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm

# Create your views here.


def register(response):

    if response.method == 'POST':
        # build in django usercreation form
        form = RegisterForm(response.POST)
        # validate form
        if form.is_valid():
            # save form
            form.save()
        return redirect('/')
    else:
        form = RegisterForm()

    return render(response, 'register/register.html', {'form': form})
