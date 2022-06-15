import json

from django import forms
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

from webapp import models
from webapp.utils.bootstrap import BootStrapModelForm
from webapp.utils.pagination import Pagination


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            "detail": forms.TextInput
        }


def task_list(request):
    """任务列表"""

    data_dict = {}
    value = request.GET.get('q')
    if value:
        data_dict["account__contains"] = value
    queryset = models.Task.objects.filter(**data_dict)
    search_data = value
    page_object = Pagination(request, queryset)
    form = TaskModelForm()
    context = {
        "queryset": page_object.page_queryset,
        "search_data": search_data,
        "page_string": page_object.html(),
        "form": form,
    }

    return render(request, "task_list.html", context)


@csrf_exempt
def task_ajax(request):
    data_dict = {"status": True, 'data': [11, 22, 33, 44]}
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def task_add(request):
    form = TaskModelForm(data=request.POST)
    print(request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


def task_delete(request, nid):
    models.Task.objects.filter(id=nid).delete()
    return redirect('/task/list/')
