from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from OMS.models.order import Order

@login_required(login_url="/do_login/")
def order_list(request):
    if request.method == 'GET':
        if request.user.is_staff:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)

        context = {
            'orders': orders
            }

        return render(request, 'order_list.html', context)
    else:
        return HttpResponse("Sorry, only GET is allowed", status=405)

