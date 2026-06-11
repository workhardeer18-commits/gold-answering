from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect

from OMS.models.category_product_mazaneh import CategoryProductMazaneh


@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def delete_category_mazaneh(request, mazaneh_id):

    try:
        mazaneh = CategoryProductMazaneh.objects.get(id=mazaneh_id)
    except CategoryProductMazaneh.DoesNotExist:
        messages.error(request, "Mazaneh not found")
        return redirect("category_mazane_list")

    if request.method == "POST":

        mazaneh.delete()

        messages.success(
            request,
            "مظنه با موفقیت حذف شد."
        )

        return redirect("category_mazane_list")

    else:
        return HttpResponse("Method Not Allowed", status=405)
