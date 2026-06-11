from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render
from OMS.forms.product_form import ProductForm

@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def create_product(request):
    if request.method == "GET":
        form = ProductForm()
        return render(request, 'create_product.html', {"form": form})
    elif request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'محصول با موفقیت ذخیره شد.')
            return redirect('product_list')

        else:
            messages.error(request, 'داده معتبر نیست.')
            return redirect('create_product')
    else:
        return HttpResponse('Method Not Allowed', status=405)
