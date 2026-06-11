from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from OMS.models.product import Product


@login_required(login_url="/do_login/")

def product_list(request):
    if request.method == "GET":
        context = {
            'products': Product.objects.all()
        }
        return render(request, 'product_list.html', context)
    else:
        return HttpResponse("Method Not Allowed", status=405)


