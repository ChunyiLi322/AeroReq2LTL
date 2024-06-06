import json
import os
import re

import numpy as np
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from blog.models.formalMethod import FormalMethod
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse
from django.shortcuts import render


from blog.models.requirementsdb import IPBase,IPRequirement,RQTemplate,RQWordSub
from django import forms
from blog.methods.chatgpt import textconstruct, set_textconstruct, chatgptresponse


def postIPID(req):
    # 判断请求类型
    if req.method == 'GET':
        return render(req, 'blog/nl2ltl.html')
    else:
        # 获取表单数据,如果获取不到,则为None，不用单独，NONE在get方法里面
        IPname = req.POST.get("IPname")
        print("views中postIPID获取的数据",IPname)

        IPID_index = IPBase.objects.get(name=IPname).index
        REID_list = list(IPRequirement.objects.filter(ip=IPID_index).values_list('id', flat=True))
        print("views中postIPID获取的数据IPID_index",IPID_index)
        print("views中postIPID获取的数据REID_list",REID_list)
        ret = {'REID_list': REID_list}
        print("views中postIPID获取的数据ret",ret)
    # 将列表传给模板index.html
    return HttpResponse(json.dumps(ret))


class IPREform(forms.Form):
    IPname = forms.CharField(widget=forms.Textarea)
    # print("-----------text1-----------", text1)
    REID = forms.CharField(widget=forms.Textarea)

class IPREAPIVerform(forms.Form):
    IPname = forms.CharField(widget=forms.Textarea)
    REID = forms.CharField(widget=forms.Textarea)
    API = forms.CharField(widget=forms.Textarea)
    ChatGPTVersion = forms.CharField(widget=forms.Textarea)



def get_row_data(index_value):
    try:
        # 获取 IPBase 表中的唯一一行数据
        row = RQTemplate.objects.get(index=index_value)  # 假设 index=1 为你要获取的行
        # 将行数据存储到一个列表中
        row_data_list = [getattr(row, f'content{i}') for i in range(1, 11)]  # 假设该行有 10 列，字段名为 field1, field2, ..., field10
        return row_data_list
    except RQTemplate.DoesNotExist:
        # 处理数据不存在的情况
        return []

def get_row_data_pro(index_value):
    try:
        # 获取 IPBase 表中的唯一一行数据
        row = RQTemplate.objects.get(index=index_value)  # 假设 index=1 为你要获取的行
        # 将行数据存储到一个列表中
        row_data_list = [getattr(row, f'content{i}') for i in range(1, 11)]  # 假设该行有 10 列，字段名为 field1, field2, ..., field10
        row_data_list_2 = [getattr(row, 'ltl')]
        IPTem_string_list = [str(item) if item is not None else "" for item in row_data_list]
        IPTem_string = ' '.join(IPTem_string_list)
        IPTem_string_list_2 = [str(item) if item is not None else "" for item in row_data_list_2]
        IPTem_string_2 = ' '.join(IPTem_string_list_2)
        row_data_string = IPTem_string + "，其对应ltl公式像:" + IPTem_string_2
        return row_data_string
    except RQTemplate.DoesNotExist:
        # 处理数据不存在的情况
        return []



def postIPIDREID(req):
    # 判断请求类型
    if req.method == 'GET':
        return render(req, 'blog/nl2ltl.html')
    else:
        form = IPREform(req.POST)
        # 获取表单数据和文件对象
        if form.is_valid():
            IPname = form.cleaned_data['IPname']
            REID = form.cleaned_data['REID']
            print("-----------IPname-----------", IPname)
            print("-----------REID-----------", REID)
            IPID_index = IPBase.objects.get(name=IPname).index
            RE_tem_ID = list(IPRequirement.objects.filter(ip=IPID_index,id=REID).values_list('template_id', flat=True))
            RE_list = list(IPRequirement.objects.filter(ip=IPID_index,id=REID).values_list('requirement', flat=True))
            IPTem_string_list = get_row_data(int(RE_tem_ID[0]))
            print("-----------RE_tem_ID-----------", RE_tem_ID[0])
            print("-----------RE_list-----------", RE_list[0])
            print("-----------IPTem_string-----------", type(IPTem_string_list),IPTem_string_list)
            IPTem_string_list = [str(item) if item is not None else "" for item in IPTem_string_list]
            IPTem_string = ' '.join(IPTem_string_list)
            print("-----------IPTem_string-----------", IPTem_string)
            # 改变输入给大模型的提示，加上样本提示
            TEM_value = get_row_data_pro(int(RE_tem_ID[0]))
            set_textconstruct("You know "+TEM_value)

            ret = {'ExsitID': RE_list[0], 'IPTem_string':IPTem_string}
            return HttpResponse(json.dumps(ret))
        else:
            # 创建一个空的表单
            return HttpResponse('查询失败！')


# 模板借助大模型自动生成

def postIPIDreturnLLMTem(req):
    # 判断请求类型
    if req.method == 'GET':
        return render(req, 'blog/nl2ltl.html')
    else:
        # 获取表单数据和文件对象
        form = IPREAPIVerform(req.POST)
        # 获取表单数据和文件对象
        if form.is_valid():
            IPname = form.cleaned_data['IPname']
            REID = form.cleaned_data['REID']
            API = form.cleaned_data['API']
            ChatGPTVersion = form.cleaned_data['ChatGPTVersion']
            print("-----postIPIDreturnLLMTem------API-----------", API)
            print("-----postIPIDreturnLLMTem------ChatGPTVersion-----------", ChatGPTVersion)
            IPID_index = IPBase.objects.get(name=IPname).index
            RE_tem_ID = list(IPRequirement.objects.filter(ip=IPID_index,id=REID).values_list('template_id', flat=True))
            RE_list = list(IPRequirement.objects.filter(ip=IPID_index,id=REID).values_list('requirement', flat=True))
            print("-------postIPIDreturnLLMTem----RE_tem_ID-----------", RE_tem_ID[0])
            print("------postIPIDreturnLLMTem-----RE_list-----------", RE_list[0])
            template_string = chatgptresponse(str(ChatGPTVersion),API,RE_list[0])
            ret = {'NewTem': template_string}

            # 改变输入给大模型的提示，加上样本提示
            TEM_value = get_row_data_pro(int(RE_tem_ID[0]))
            set_textconstruct("You know "+TEM_value)

            return HttpResponse(json.dumps(ret))
        else:
            # 创建一个空的表单
            return HttpResponse(json.dumps('查询失败'))


def WordSubstitution(req):
    # 判断请求类型
    if req.method == 'GET':
        return render(req, 'log/nl2ltl.html')
    else:
        # 获取表单数据,如果获取不到,则为None，不用单独，NONE在get方法里面
        constraintnl = req.POST.get("constraintnl")
        print("接受到的constraintnl",constraintnl)
        # 数据预处理
        Chname_list = list(RQWordSub.objects.values_list('chname', flat=True))
        Engname_list = list(RQWordSub.objects.values_list('engname', flat=True))
        newtext = replace_words(constraintnl,Chname_list,Engname_list)
        # 传回
        ret = {'newtext': newtext}
        print("----------newtext---------------",newtext)
    # 将列表传给模板index.html
    return HttpResponse(json.dumps(ret))

def replace_words(string, list_A, list_B):
    # 将单词列表A转换为正则表达式模式，用于匹配中文单词
    pattern = '|'.join(re.escape(word) for word in list_A)

    # 匹配中文单词并替换
    def replace(match):
        # 找到匹配的单词在列表A中的位置，并返回列表B中对应位置的单词
        return list_B[list_A.index(match.group(0))]

    # 使用sub方法替换匹配的中文单词
    result = re.sub(pattern, replace, string)

    return result


# 新的需求查找数据库相似的文本

def postnreq2tem(req):
    if req.method == 'GET':
        return render(req, 'blog/nl2ltl.html')
    else:
        # 获取表单数据,如果获取不到,则为None，不用单独，NONE在get方法里面
        NewRequirement = req.POST.get("NewRequirement")
        print("retemplate中NewRequirement获取的数据",NewRequirement)

        #首先 根据文本NewRequirement在数据库iprequiremment表的requirement的列找出最相似的文本的项，并返回该文本的值和所在行iprequiremment表的template_id的列的值

        requirements = IPRequirement.objects.values('requirement', 'template_id')

        # 提取文本列表和对应的template_id列表
        text_data = [item['requirement'] for item in requirements]
        template_ids = [item['template_id'] for item in requirements]

        # 将new_requirement添加到文本列表中
        text_data.append(NewRequirement)

        # 使用TF-IDF向量化文本数据
        vectorizer = TfidfVectorizer().fit_transform(text_data)
        vectors = vectorizer.toarray()

        # 计算新文本与其他文本的余弦相似度
        cosine_matrix = cosine_similarity(vectors)

        # 获取新文本与所有文本的相似度（新文本是最后一个向量）
        similarity_scores = cosine_matrix[-1][:-1]

        # 找到最相似文本的索引
        most_similar_index = np.argmax(similarity_scores)

        # 返回最相似文本和对应的template_id
        most_similar_text = text_data[most_similar_index]
        most_similar_template_id = template_ids[most_similar_index]

        print("-----------most_similar_text-----------", most_similar_text)
        print("-----------most_similar_template_id-----------", most_similar_template_id)


        IPTem_string_list = get_row_data(int(most_similar_template_id))

        print("-----------IPTem_string-----------", type(IPTem_string_list),IPTem_string_list)
        IPTem_string_list = [str(item) if item is not None else "" for item in IPTem_string_list]
        IPTem_string = ' '.join(IPTem_string_list)
        print("-----------IPTem_string-----------", IPTem_string)



        # 改变输入给大模型的提示，加上样本提示
        TEM_value = get_row_data_pro(int(most_similar_template_id))
        set_textconstruct("You know "+TEM_value)

        print("-----------TEM_value-----------", TEM_value)


        ret = {'ExsitID': most_similar_text, 'IPTem_string':IPTem_string}
        return HttpResponse(json.dumps(ret))