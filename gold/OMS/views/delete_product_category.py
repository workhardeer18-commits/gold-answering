from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

from OMS.models.product_category import ProductCategory

@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def delete_product_category(request, pk):
    try:
       instance = ProductCategory.objects.get(id=pk)
       instance.delete()
       messages.success(request, 'دسته بندی محصول با موفقیت حذف شد.')
       return redirect('product_category_list')
    except ProductCategory.DoesNotExist:
        messages.error(request, 'اطلاعات صحیح نیست')
        return redirect('product_category_list')

