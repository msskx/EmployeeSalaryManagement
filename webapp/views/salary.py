from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
import json

from webapp import models
from webapp.utils.bootstrap import BootStrapForm, BootStrapModelForm
from webapp.utils.pagination import Pagination


class SalaryModelForm(BootStrapModelForm):
    class Meta:
        model = models.Salary
        # fields = "__all__"
        fields = ["basic_salary", "welfare_allowance", "bonus_salary", "unemployment_insurance", "housing_fund", "acc"]


class SalaryEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Salary
        # fields = "__all__"
        fields = ["basic_salary", "welfare_allowance", "bonus_salary", "unemployment_insurance", "housing_fund"]


def salary_list(request):
    """工资列表"""

    data_dict = {}
    value = request.GET.get('q')
    if value:
        data_dict["acc_id"] = value

    queryset = models.Salary.objects.filter(**data_dict).order_by("salary_sum")
    search_data = value
    page_object = Pagination(request, queryset)
    form = SalaryModelForm()
    context = {
        "queryset": page_object.page_queryset,
        "search_data": search_data,
        "page_string": page_object.html(),
        "form": form,

    }

    return render(request, "salary_list.html", context)


@csrf_exempt
def salary_add(request):
    form = SalaryModelForm(data=request.POST)
    datas = request.POST
    # 取到提交的内容
    for item in datas:
        print(item, "+", datas[item])
        sum = float(datas['basic_salary']) + float(datas['welfare_allowance']) + float(datas['bonus_salary']) - float(
            datas['unemployment_insurance']) - float(datas['housing_fund'])
    if form.is_valid():
        form.save()
        # 给总数赋值
        models.Salary.objects.filter(acc=datas['acc']).update(salary_sum=sum)

        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


@csrf_exempt
def salary_edit(request, nid):
    row_object = models.Salary.objects.filter(id=nid).first()
    datas = request.POST
    # 取到提交的内容
    for item in datas:
        print(item, "+", datas[item])
        sum = float(datas['basic_salary']) + float(datas['welfare_allowance']) + float(datas['bonus_salary']) - float(
            datas['unemployment_insurance']) - float(datas['housing_fund'])
    if request.method == "GET":
        # 根据ID去数据库获取要编辑那一行的数据（对象）
        form = SalaryEditModelForm(instance=row_object)

        return render(request, 'salary_edit.html', {'form': form})
    form = SalaryEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():  # 数据校验通过
        form.save()
        models.Salary.objects.filter(id=nid).update(salary_sum=sum)
        return redirect('/salary/list/')
    return render(request, 'salary_edit.html', {"form": form})
    pass


def salary_delete(request, nid):
    """ 删除管理员 """
    models.Salary.objects.filter(id=nid).delete()
    return redirect('/salary/list/')


def salary_chart(request):
    datas = models.DepartSalary.objects.all()
    dict = {}
    for item in datas:
        dict[item.title] = 0
    for item in datas:
        dict[item.title] += item.salary_sum
    print(dict)
    depart_name = []
    depart_salary = []

    pie = []
    for k in dict:
        depart_name.append(k)
        dict[k] = float(dict[k])
        depart_salary.append(dict[k])
        pie.append(
            {"value": dict[k], "name": k}
        )

    context = {
        "depart_name": depart_name,
        "depart_salary": depart_salary,
        "pie": pie
    }
    return render(request, "salary_chart.html", context)
