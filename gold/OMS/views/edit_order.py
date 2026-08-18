from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from OMS.forms.order_status_form import OrderStatusForm
from OMS.models.order import Order


@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def edit_order(request, pk):
    order = get_object_or_404(Order, id=pk)

    if request.method == "POST":
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            new_status = form.cleaned_data.get("status")


            if new_status == "approved":
                is_expired = timezone.now() > (order.created_at + timedelta(seconds=30))
                if is_expired:
                    order.status = "rejected"
                    order.save(update_fields=["status", "updated_at"])
                    messages.error(request, "مهلت ۳۰ ثانیه‌ای تایید سفارش به پایان رسیده و سفارش رد شد.")
                    return redirect("order_list")

            form.save()
            messages.success(request, "وضعیت سفارش با موفقیت به‌روزرسانی شد.")
            return redirect("order_list")
    else:
        form = OrderStatusForm(instance=order)

    return render(request, "edit_order.html", {"form": form, "order": order})