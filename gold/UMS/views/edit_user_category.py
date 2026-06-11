from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, request
from django.shortcuts import redirect, render
from UMS.forms.user_category_form import UserCategoryForm
from UMS.models.user_category import UserCategory

@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def edit_user_category(request, pk):
    instance = UserCategory.objects.get(id=pk)

    if request.method == 'GET':
        form = UserCategoryForm(instance=instance)
        return render(request, 'edit_user_category_list.html', {'form': form})
    elif request.method == 'POST':
        form = UserCategoryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'دسته بندی کاربر با موفقیت ویرایش شد.')
            return redirect('user_category_list')
        else:
            messages.error(request, 'اطلاعات صحیح نیست.')
            return redirect('edit_user_category')
    else:
        return HttpResponse('Method Not Allowed', status=405)
