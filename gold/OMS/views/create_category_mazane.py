from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render
from OMS.forms.CategoryProductMazanehForm import CategoryProductMazanehForm



@login_required(login_url="/do_login/")
@user_passes_test(lambda u: u.is_staff)
def create_category_mazaneh(request):
    if request.method == 'GET':
        form = CategoryProductMazanehForm()
        return render(request, 'create_category_mazaneh.html', {'form': form})
    elif request.method == "POST":
        form = CategoryProductMazanehForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "مظنه با موفقیت ثبت شد")
            return redirect("category_mazane_list")
        else:
            messages.error(request, "اطلاعات صحیح نیست .")
            return redirect("create_category_mazaneh")
    else:
         return HttpResponse(request, 'Method Not Allowed', status=405)
