from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from UMS.forms.user_profile import UserProfileForm
from UMS.models.user import User


@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def edit_user(request, user_id):

    user = get_object_or_404(User, id=user_id)

    if request.method == "GET":
        form = UserProfileForm(instance=user)
        return render(request, "create_user.html", {"form": form, "user_obj": user})
    elif request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "فرم با موفقیت ذخیره شد.")
            return redirect("admin_users")
        else:
            messages.error(request, "اطلاعات صحیح نیست.")
            return redirect("edit_users")

    return HttpResponse("Method Not Allowed", status=405)
