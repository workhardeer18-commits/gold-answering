from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render

from OMS.forms.CategoryProductMazanehForm import CategoryProductMazanehForm
from OMS.models.product_category import ProductCategory




@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def edit_product_category(request, pk):
    instance = ProductCategory.objects.get(id=pk)
    if request.method == 'GET':
        form = CategoryProductMazanehForm(instance=instance)
        return render(request, 'edit_product_category.html', {"form": form})
    elif request.method == 'POST':
        form = CategoryProductMazanehForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'دسته بندی محصول با موفقیت تغییر یافت.')
            return redirect('product_category_list')
        else:
            messages.error(request, 'اطلاعات صحیح نیست.')
            return redirect('edit_product_category')

    else:
        return HttpResponse('Method Not Allowed', status=405)
