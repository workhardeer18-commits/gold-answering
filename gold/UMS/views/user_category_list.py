from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from UMS.models.user_category import UserCategory

@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def user_category_list(request):
    if request.method == 'GET':
        context = {
            'categories' : UserCategory.objects.all()
        }
        return render(request, 'user_category_list.html', context)
    else:
        return HttpResponse('Method Not Allowed', status=405)
