from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

from OMS.models.category_product_mazaneh import CategoryProductMazaneh



@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def category_mazane_list(request):
    if request.method == 'GET':
        context = {
            'mazane_list' : CategoryProductMazaneh.objects.all(),
        }
        return render(request, 'category_mazane_list.html', context)
    else:
        return HttpResponse(request, "Method Not Allowed", status=405)
