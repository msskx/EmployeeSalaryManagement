
from django.shortcuts import render, redirect
from webapp import models

# Create your views here.
from webapp.utils.form import UserModelForm
from webapp.utils.pagination import Pagination




def user_list(request):
    data_dict = {}
    value = request.GET.get('q')
    if value:
        data_dict["mobile__contains"] = value
    queryset = models.UserInfo.objects.filter(**data_dict)
    search_data = value
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "search_data": search_data,
        "page_string": page_object.html(),

    }

    return render(request, "user_list.html", context)


def user_add(request):
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all(),
        }
        return render(request, 'user_add.html', context)

    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender_id = request.POST.get('gd')
    depart = request.POST.get('dp')
    models.UserInfo.objects.create(name=user, password=pwd, age=age, account=account,
                                   create_time=ctime, gender=gender_id, depart_id=depart)
    return redirect("/user/list/")


def user_model_form_add(request):
    if request == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    row_object = models.UserInfo.objects.filter(account=nid).first()
    if request.method == "GET":
        # 根据ID去数据库获取要编辑那一行的数据（对象）
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():  # 数据校验通过
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(account=nid).delete()
    return redirect('/user/list/')