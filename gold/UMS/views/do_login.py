from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render


def do_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'اطلاعات صحیح نیست .')
            return redirect('do_login')
        else:
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, 'به پنل ادمین خوش آمدید . ')
                return redirect('admin_dashboard')
            else:

                login(request, user)
                messages.success(request, 'خوش آمدید . ')
                return redirect('user_dashboard')
    else:
         return HttpResponse('Method not allowed', status=405)
