import re

import openai


textconstruct = "Please answer the logical formula, the formulas are all wrapped in $$ $$, and explain the meaning of the formula."

def askChatGPT(messages,MODEL):
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages = messages,
        temperature=0)
    return response['choices'][0]['message']['content']


def find_longest_n(strings, n):
  # 初始化一个空列表，用来存储最长的几个字符串
  longest = []
  # 遍历字符串列表
  for s in strings:
    # 如果最长列表还没有达到n个，直接将当前字符串加入
    if len(longest) < n:
      longest.append(s)
    # 否则，找出最长列表中最短的字符串
    else:
      shortest = min(longest, key=len)
      # 如果当前字符串比最短的字符串长，用当前字符串替换最短的字符串
      if len(s) > len(shortest):
        longest[longest.index(shortest)] = s
  # 返回最长列表
  return longest

def set_textconstruct(new_value):
    global textconstruct
    textconstruct = new_value + "Please answer the logical formula, the final formula are all wrapped in $$ $$, and explain the meaning of the formula."



def chatgptresponse1(MODEL,api_key,text,flcheckbox,flpracheckbox):
    # api_key = ""
    print("----------------0---------------------------")
    openai.api_key = api_key
    path_to_file = "test"
    print("----------------1---------------------------")
    messages = [{"role": "system","content":"You are a mature professional scholar of formalization, mastering"+flcheckbox+"，and the knowledge of"+flpracheckbox+".Translate the following natural language sentences into an LTL formula and explain your translation step by step. Remember that X means \"next\", U means \"until\", G means \"globally\", F means \"finally\", GF means \"infinitely often\",\"&\" means \"conjunction\", \"|\" means \"disjunction\", \"!\" means \"not\", \" ->\" means \"implication\", \"<->\" means \"equivalence\"."}]
    text1 = textconstruct + " The input requirement is :" + text
    print("----------------textconstruct---------------------------",textconstruct)
    d = {"role":"user","content":text1}
    messages.append(d)
    print("----------------2---------------------------")
    text_respon = askChatGPT(messages,MODEL)
    print("----------------3---------------------------")
    d = {"role":"assistant","content":text_respon}
    print('chatgpt：'+text1+'\n')
    messages.append(d)
    print("messages",messages)
    text_response = re.findall(r'\$\$([^\$]*)\$\$', text_respon)
    fl = '.\n'.join(text_response).replace("\&","&")
    print("------------公式到前端---------------",fl)
    return fl, text_respon


def chatgptresponse(MODEL,api_key,text):
    openai.api_key = api_key
    messages = [{"role": "system","content": "What is the writing template for this statement, and what is the LTL formula corresponding to the template? In the template, professional-related descriptions are replaced by Domain-nouns, working mode is replaced by Workmode, and conditions are replaced by Condition. The output is expressed as [*template*];[*$$LTL formula$$*]."}]
    d = {"role":"user","content":text}
    messages.append(d)
    print("----------------4---------------------------")
    text_respon = askChatGPT(messages,MODEL)
    d = {"role":"assistant","content":text_respon}
    print('chatgpt：'+text+'\n')
    messages.append(d)
    print("text_respon",text_respon)
    extracted_strings = re.findall(r'\[\*(.*?)\*\]', text_respon)
    print("---------------------------------",extracted_strings)
    return extracted_strings[0]
