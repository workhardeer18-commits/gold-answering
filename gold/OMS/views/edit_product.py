from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render
from OMS.forms.product_form import ProductForm
from OMS.models.product import Product

@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def edit_product(request, pk):
    instance = Product.objects.get(id=pk)
    if request.method == 'GET':
        form = ProductForm(instance=instance)
        return render(request, 'edit_product.html', {"form": form})
    elif request.method == 'POST':

        form = ProductForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'محصول با موفقیت ذخیره شد.')
            return redirect('product_list')
        else:
            messages.error(request, 'اطلاعات صحیح نیست.')
            return redirect('edit_product')
    else:
        return HttpResponse('Method not allowed', status=405)
