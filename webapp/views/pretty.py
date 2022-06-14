from django.shortcuts import render, redirect
from webapp import models

# Create your views here.
from webapp.utils.form import PrettyModelForm, PrettyEditModelForm
from webapp.utils.pagination import Pagination

def pretty_list(request):
    """靓号列表"""
    data_dict = {}
    value = request.GET.get('q')
    if value:
        data_dict["mobile__contains"] = value
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")
    search_data = value
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "search_data": search_data,
        "page_string": page_object.html(),

    }
    return render(request, "pretty_list.html", context)



def pretty_add(request):
    if request == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, "pretty_add.html", {"form": form})

    pass


def pretty_edit(request, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据ID去数据库获取要编辑那一行的数据（对象）
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():  # 数据校验通过
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {"form": form})
    pass

def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
