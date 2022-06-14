from django.db import models


# Create your models here.
class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(verbose_name="用户名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """

    account = models.CharField(verbose_name="员工工号", max_length=16, primary_key=True)
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    create_time = models.DateTimeField(verbose_name="入职时间")
    # 无约束
    # depart_id=models.BigIntegerField(verbose_name="部门ID")
    # 有约束
    # -to,与哪张表关联
    # -to_field,表中哪一列关联
    # Django自动
    # 写的depart生成数据列depart_id
    # 删除后操作
    ###级联删除
    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    ###置空
    occupation_choices = (
        (1, "经理"),
        (2, "工程师"),
        (3, "销售员"),
        (4, "测试"),
        (5, "产品"),
        (6, "售后"),
    )
    occupation = models.SmallIntegerField(verbose_name="职业", choices=occupation_choices, default=1)

    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    # Django约束
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, default=1)

    def __str__(self):
        return self.account


class PrettyNum(models.Model):
    """ 靓号表 """

    mobile = models.CharField(verbose_name="手机号", max_length=11, unique=True)

    price = models.IntegerField(verbose_name="价格", default=0)
    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
        (5, "5级"),
    )

    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未占用"),
    )

    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Task(models.Model):
    """ 任务 """
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=3)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Salary(models.Model):
    """工资表"""

    """基本工资、福利补贴、奖励工资，失业保险、住房公积金"""
    basic_salary = models.DecimalField(verbose_name="基本工资", max_digits=10, decimal_places=2, default=0)
    welfare_allowance = models.DecimalField(verbose_name="福利补贴", max_digits=10, decimal_places=2, default=0)
    bonus_salary = models.DecimalField(verbose_name="奖励工资", max_digits=10, decimal_places=2, default=0)
    unemployment_insurance = models.DecimalField(verbose_name="失业保险", max_digits=10, decimal_places=2, default=0)
    housing_fund = models.DecimalField(verbose_name="住房公积金", max_digits=10, decimal_places=2, default=0)
    salary_sum = models.DecimalField(verbose_name="实发工资", max_digits=10, decimal_places=2, default=0)
    acc = models.OneToOneField(verbose_name="员工工号", to="UserInfo", unique=True, to_field='account',
                               on_delete=models.CASCADE)


class DealWithLog(models.Model):
    '''日志表'''
    name = models.CharField(verbose_name="操作名称", max_length=32)
    time = models.TimeField(verbose_name="操作时间")
    details = models.TextField(verbose_name="详细信息", max_length=128)


class DepartSalary(models.Model):

    """视图"""
    account = models.CharField(verbose_name="员工工号", max_length=16, primary_key=True)
    salary_sum = models.DecimalField(verbose_name="实发工资", max_digits=10, decimal_places=2, default=0)
    title = models.CharField(verbose_name="标题", max_length=32)

    class Meta:
        # managed = False

        db_table = "departSalary"
