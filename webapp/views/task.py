import json

from django import forms
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from webapp import models
from webapp.utils.bootstrap import BootStrapModelForm


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            "detail": forms.TextInput
        }


def task_list(request):
    """任务列表"""

    form = TaskModelForm()
    return render(request, "task_list.html", {"form": form})


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
