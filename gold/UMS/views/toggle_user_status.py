from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST


from UMS.models.user import User


@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
@require_POST
def toggle_user_status(request, user_id):

    user = get_object_or_404(User, id=user_id)

    if user.is_superuser or user.is_staff:
        messages.error(request, "وضعیت ادمین قابل تغییر نیست.")
        return redirect("admin_users")

    if user == request.user:
        messages.error(request, "نمی‌توانید خودتان را غیرفعال کنید.")
        return redirect("admin_users")

    user.is_active = not user.is_active
    user.save()

    return redirect("admin_users")
