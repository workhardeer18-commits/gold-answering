from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from UMS.models.user import User


@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def delete_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        if user.is_superuser:
            messages.error(request, "سوپر ادمین قابل حذف نیست.")
            return redirect("admin_users")

        user.delete()
        messages.success(request, "کاربر حذف شد.")
        return redirect('admin_users')

    return HttpResponse('Method Not Allowed', status=405)
