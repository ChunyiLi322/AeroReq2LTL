# 导入必要的模块
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import os

from django.views.decorators.csrf import csrf_exempt

from blog.models.formalMethod import FormalMethod
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse
from django.shortcuts import render

# 定义一个文件上传表单
from django import forms

from blog.methods.computesim import compute_sim
from blog.methods.pdf2txt import file2textlist

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_dir = BASE_DIR + '\\requirement\\'
MEDIA_ROOT = os.path.join(path_dir)
print("-----------path_dir-----------",path_dir)
class file2nlreq(forms.Form):
    file = forms.FileField()
    text1 = forms.CharField(widget=forms.Textarea)
    # print("-----------text1-----------", text1)
    text2 = forms.CharField(widget=forms.Textarea)

# 定义一个文件上传视图函数
@csrf_exempt
def filesolve(req):
    if req.method == 'GET':
        return render(req, 'blog/nl2ltl.html')
    else:
        form = file2nlreq(req.POST, req.FILES)
        print("-------------------form.is_valid()-------------------",form.is_valid())
        # 获取表单数据和文件对象
        if form.is_valid():
            file = form.cleaned_data['file']
            text1 = form.cleaned_data['text1']
            text2 = form.cleaned_data['text2']
            # print("进入了form.is_valid()--------------------------")
            print("-----------text1-----------", text1)
            print("-----------text2-----------", text2)
            # 将文件保存到指定的位置
            with open(os.path.join(MEDIA_ROOT, file.name), 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            try:
                # test_list=file2textlist(file.name, 15, 16)
                text_list = file2textlist(file.name, int(text1), int(text2))
                print("-----------文件可转化语句--------------",'.\n'.join(text_list))
                # 返回上传成功的信息
                ret = {'text_list': text_list}
                return HttpResponse(json.dumps(ret))
            # 返回一个文件上传页面
            except:
                return HttpResponse('文件非pdf格式！')
        else:
            # 创建一个空的表单
            return HttpResponse('文件上传失败！')


#10-21
def computesim(req):
    # 判断请求类型
    if req.method == 'GET':
        return render(req, 'blog/nl2ltl.html')
    else:
        # 获取表单数据,如果获取不到,则为None，不用单独，NONE在get方法里面
        textcheckbox = req.POST.get("textcheckbox")
        text = json.loads(textcheckbox)
        textliststring = '.\n'.join(text)
        print("---------------------text------------------------",text)
        print("---------------------text------------------------",type(text))
        simvalue = compute_sim(text)
        print("---------------------simvalue------------------------", simvalue)
        ret = {'simvalue': simvalue , 'nlmessage': textliststring}
    # 将列表传给模板index.html
    return HttpResponse(json.dumps(ret))
