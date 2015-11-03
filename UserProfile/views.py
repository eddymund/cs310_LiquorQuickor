from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout

from .forms import SignUpForm


class ProfileView(TemplateView):
    """
    A view of the users profile. If no user is logged in propts user to create
    a profile
    """
    # TODO: create link to profile creation page
    # TODO: beautify profile and display user image
    template_name = 'UserProfile/profile.html'


class Login(TemplateView):
    """
    A form for logging a user into the app
    """
    template_name = 'UserProfile/login.html'


# from django docs
def auth_user(request):
    """
    Authenticates and logs in a user to the site using the username and
    password in POST.
    :param request:
    :return: HttpResponse
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('profile:profile'))
        else:
            # TODO: Inform user no longer active
            return HttpResponseRedirect(reverse('profile:login'))
    else:
        # TODO: Inform user login failed
        return HttpResponseRedirect(reverse('profile:login'))


def sign_up(request):
    if request.method == 'POST':
        return register(request)
    form = SignUpForm()
    return render(request, 'UserProfile/signup.html', {"form": form})


def register(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.save()
        new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
        login(request, new_user)
        return redirect('map:map')
    else:
        return redirect('profile:signup')

def logout_view(request):
    logout(request)
    return redirect('map:map')