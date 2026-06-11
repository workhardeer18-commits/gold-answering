from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from UMS.models.user import User


@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def admin_users(request):
    search = request.GET.get("search", "")

    users = User.objects.order_by("-date_joined")

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(profile__phone_number__icontains=search)
        )

    paginator = Paginator(users,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request,"users.html",{
        "page_obj":page_obj,
        "search":search
    })

