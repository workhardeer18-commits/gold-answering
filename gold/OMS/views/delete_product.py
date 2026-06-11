from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

from OMS.models.product import Product


@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def delete_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        messages.success(request, 'محصول با موفقیت حذف شد.')
        return redirect('product_list')
    except Product.DoesNotExist:
        messages.error(request, 'محصول یافت نشد.')
        return redirect('product_list')



