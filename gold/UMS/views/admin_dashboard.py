from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    if request.method == 'GET':
        return render(request, "admin_dashboard.html")
    else:
        return HttpResponse("Method Not Allowed", status=405)
