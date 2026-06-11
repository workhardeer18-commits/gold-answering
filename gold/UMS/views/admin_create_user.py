from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render
from UMS.forms.user_profile import UserProfileForm


@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def admin_create_user(request):
    if request.method == 'GET':
        form = UserProfileForm()
        return render(request, 'create_user.html', {'form': form})
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'کاربر جدید با موفقیت ساخته شد.')
            return redirect('admin_users')
        else:
            messages.error(request, "لطفاً خطاهای زیر را اصلاح کنید.")
            return render(request, 'create_user.html', {'form': form})
    else:
        return HttpResponse('Method not allowed', status=405)
