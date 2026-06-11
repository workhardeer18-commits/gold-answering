from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

from OMS.models.product_category import ProductCategory

@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def product_category_list(request):
    if request.method == 'GET':
        context = {
            'categories' : ProductCategory.objects.all(),
                }
        return render(request, 'product_category_list.html', context)
    else:
        return HttpResponse("Method Not Allowed", status=405)
