import json
import os

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from blog.models.formalMethod import FormalMethod
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse
from django.shortcuts import render

from blog.models.keyWord import KeyWord
from blog.models.requirementsdb import IPBase,IPRequirement,RQComponent,RQWorkMode,RQCondition
from blog.methods.chatgpt import chatgptresponse,chatgptresponse1
from blog.methods.latex2png import formula2png


class solveform(CreateView):
      model = FormalMethod
      fields = ['email']
      HttpResponse("Helloworld2 ! ")
      success_url = reverse_lazy('login')


def insert_to_FormalMethod_database(name):
    try:
        if not FormalMethod.objects.get(name=name):
            a = FormalMethod(name=name)
            a.save()
    except FormalMethod.DoesNotExist:
        a = FormalMethod(name=name)
        a.save()


def insert_to_KeyWord_database(name):
    try:
        if not KeyWord.objects.get(name=name):
            a = KeyWord(name=name)
            a.save()
    except KeyWord.DoesNotExist:
        a = KeyWord(name=name)
        a.save()

nl_list = []
def postnl(req):
    # 判断请求类型
    if req.method == 'GET':
        return render(req, 'blog/nl2ltl.html')
    else:
        # 获取表单数据,如果获取不到,则为None，不用单独，NONE在get方法里面
        ChatGptAPIname = req.POST.get("ChatGptAPIname")
        nlmessage = req.POST.get("nlmessage")
        flcheckbox = req.POST.get("flcheckbox")
        flpracheckbox = req.POST.get("flpracheckbox")
        ChatGptversion = req.POST.get("ChatGptversion")
        flcheckbox = predata_checkbox(flcheckbox)
        flpracheckbox = predata_checkbox(flpracheckbox)
        flmessage, flpramessage = chatgptresponse1(str(ChatGptversion), ChatGptAPIname, nlmessage, flcheckbox,
                                                  flpracheckbox)
        print(ChatGptAPIname, nlmessage, flcheckbox,'\n' , flpracheckbox, ChatGptversion)
        # 定义字典
        nl = {'ChatGptAPIname': ChatGptAPIname, 'nlmessage': nlmessage}
        # 用于test
        # ret = {'flmessage': 'flmessage', 'flpramessage': 'flpramessage'}
        ret = {'flmessage': flmessage, 'flpramessage': flpramessage}
    # 将列表传给模板index.html
    return HttpResponse(json.dumps(ret))

def postflimg(req):
    # 判断请求类型
    if req.method == 'GET':
        return render(req, 'log/nl2ltl.html')
    else:
        # 获取表单数据,如果获取不到,则为None，不用单独，NONE在get方法里面
        flmessage = req.POST.get("flmessage")
        flpramessage = req.POST.get("flpramessage")
        print("接受到的flmessage",flmessage)
        print("接受到的flpramessage", flpramessage)
        # 数据预处理
        formula2png(flmessage)
        # 传到生成Img的方法
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pathdir = '/static/blog/images/home/fl.png'
        ret = {'pathdir': pathdir}
    # 将列表传给模板index.html
    return HttpResponse(json.dumps(ret))



def predata_checkbox(flcheckbox):
    flcheckbox = flcheckbox.replace("[", "")
    flcheckbox = flcheckbox.replace("\"", "")
    flcheckbox = flcheckbox.replace("]", "")
    flcheckbox = flcheckbox.replace(",", "和")
    return flcheckbox


def hello(request):

    # 在页面加载主题和关键字
    # formal_method_list = ['线性时序逻辑-LTL','计算树逻辑-CTL',
    #                       '命题投影时序逻辑-PPTL','行为时序逻辑-TLA',
    #                       'Petri网-PetriNet','通信顺序进程-CSP','通信系统演算-CCS']
    # for i in formal_method_list:
    #     insert_to_FormalMethod_database(i)
    FormalMethod_list = FormalMethod.objects.all()


    # key_word_list = ['软件开发','形式化验证','形式化规约','工业用途',
    #                  '形式化需求','综合形式化方法','形式化综述','数字逻辑',
    #                  '规范化语言','形式化应用','形式化方法实践与经验','形式化方法艺术',
    #                   '轻量级形式化方法','时序逻辑','归纳推理','计算机科学','控制系统',
    #                   '系统早期验证','生物调控网络','通信协议规范','网络验证'
    #                  ]
    # for i in key_word_list:
    #     insert_to_KeyWord_database(i)
    KeyWord_list = KeyWord.objects.all()

    IPID_list = IPBase.objects.values_list('name', flat=True)
    REID_list = IPRequirement.objects.filter(ip=1).values_list('id', flat=True)
    WKmode_list = RQWorkMode.objects.values_list('name', flat=True)
    RQCmode_list = RQComponent.objects.values_list('name', flat=True)
    RQCcondition_list = RQCondition.objects.values_list('name', flat=True)


    return render(request, "blog/nl2ltl.html", {"views_list": FormalMethod_list, "views_list_1": KeyWord_list, "IPID_item": IPID_list, "REID_item": REID_list, "WKmode_item":WKmode_list, "RQCmode_item":RQCmode_list, "RQCcondition_item":RQCcondition_list} )

