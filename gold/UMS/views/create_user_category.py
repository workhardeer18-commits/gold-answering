from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render
from UMS.forms.user_category_form import UserCategoryForm

@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def create_user_category(request):
    if request.method == 'GET':
        form = UserCategoryForm
        return render(request, 'create_user_category.html', {"form": form})
    elif request.method == 'POST':
        form = UserCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ' دسته بندی کاربر با موفقیت ساخته شد.')
            return redirect('user_category_list')
        else:
            messages.error(request, 'اطلاعات صحیح نیست .')
            return redirect('create_user_category')
    else:
        return HttpResponse('Method Not Allowed', status=405)
