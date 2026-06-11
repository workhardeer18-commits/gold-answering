from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


def do_logout(request):
    logout(request)
    messages.success(request, 'خارج شدید.')
    return redirect('do_login')
