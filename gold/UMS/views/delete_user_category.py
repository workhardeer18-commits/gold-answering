from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

from UMS.models.user_category import UserCategory


@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def delete_user_category(request, pk):
    try:
        instance = UserCategory.objects.get(id=pk)
        instance.delete()
        messages.success(request, "دسته بندی کاربر با موفقیت حذف شد.")
        return redirect('user_category_list')
    except UserCategory.DoesNotExist:
        messages.error(request, "دسته بندی کاربر یافت نشد.")
        return redirect('user_category_list')


