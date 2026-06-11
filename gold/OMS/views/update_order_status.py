from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render

from OMS.forms.order_status_form import OrderStatusForm
from OMS.models.order import Order


@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def update_order_status(request, order_id):

    order = Order.objects.get(id=order_id)

    if request.method == "POST":
        form = OrderStatusForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            messages.success(request, "وضعیت سفارش با موفقیت تغییر پیدا کرد.")
            return redirect('order_list')

    else:
        form = OrderStatusForm(instance=order)

    return render(request, "update_order_status.html", {
        "form": form,
        "order": order
    })
