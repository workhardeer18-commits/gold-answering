from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render

from OMS.forms.CategoryProductMazanehForm import CategoryProductMazanehForm


@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def create_product_category(request):
    if request.method == "GET":
        form = CategoryProductMazanehForm()
        return render(request, 'create_product_category.html', {"form": form})
    elif request.method == "POST":
        form = CategoryProductMazanehForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'دسته بندی محصول با موفقیت ذخیره شد.')
            return redirect('product_category_list')
        else:
            messages.error(request, 'اطلاعات صحیح نیست')
            return redirect('create_product_category')
    else:
         return HttpResponse('Method Not Allowed', status=405)
