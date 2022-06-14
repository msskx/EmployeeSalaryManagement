from django.shortcuts import render, redirect
from webapp import models

# Create your views here.
from webapp.utils.pagination import Pagination


def depart_list(request):
    # 获取部门数据
    queryset = models.Department.objects.all()
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request, "depart_list.html", context)


def depart_add(request):
    if request.method == 'GET':
        return render(request, "depart_add.html")
    if request.method == 'POST':
        title = request.POST.get("title")
        models.Department.objects.create(title=title)
        return redirect("/depart/list/")


def depart_delete(request):
    nid = request.GET.get('nid')

    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    # 根据id获取数据
    row_object = models.Department.objects.filter(id=nid).first()
    if request.method == "GET":
        return render(request, "depart_edit.html", {"row_object": row_object})
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list")
