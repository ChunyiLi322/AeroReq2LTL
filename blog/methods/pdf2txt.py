import os
import re

import pdfplumber
import jieba
import re




# TAISOU
# def find_sentences(string):
#     # 初始化一个空列表，用来存储句子
#     sentences = []
#     # print("-----------------------------sentences-----------------------",sentences)
#     # # 初始化一个空字符串，用来拼接句子
#     # sentence = ""
#     # # 遍历字符串中的每个字符
#     # for i, char in enumerate(string):
#     #     # 如果字符是大写字母，并且下一个字符不是数字，说明是句子的开头，清空之前的句子
#     #     if char == " " and (i < len(string) - 1 and string[i + 1].isupper()):
#     #         sentence = ""
#     #     # 将字符加入到句子中
#     #     sentence += char
#     #     # 如果字符是句号或者分号，说明是句子的结尾，将句子加入到列表中
#     #     if char == "." or char == ";":
#     #         sentences.append(sentence)
#     # 返回句子列表
#     # sentences = string.split('. ')
#     sentences = string.split('\n')
#     return [s + "." for s in sentences]



# NASA
def find_sentences(string):
    # 初始化一个空列表，用来存储句子
    sentences = []
    print("-----------------------------sentences-----------------------",sentences)
    # 初始化一个空字符串，用来拼接句子
    sentence = ""
    # 遍历字符串中的每个字符
    for i, char in enumerate(string):
        # 如果字符是大写字母，并且下一个字符不是数字，说明是句子的开头，清空之前的句子
        if char == " " and (i < len(string) - 1 and string[i + 1].isupper()):
            sentence = ""
        # 将字符加入到句子中
        sentence += char
        # 如果字符是句号或者分号，说明是句子的结尾，将句子加入到列表中
        if char == "." or char == ";":
            sentences.append(sentence)
    # 返回句子列表
    sentences = string.split('. ')
    # sentences = string.split('\n')
    return [s + "." for s in sentences]

def replace_newline(string):
    # 使用 replace 方法，将字符串中的 "\n" 替换为空格
    print("-------文档最初始的句子---------", string)
    # new_string = string.replace("\n", " ")
    new_string = string.replace(".\n", ". ")
    new_string = new_string.replace(".", ". ")
    new_string = remove_space_after_decimal(new_string)
    print("---------new_string-----------")
    print(new_string)
    new_string = new_string.replace("  ", " ")
    # 返回新的字符串
    # print("---------new_string-----------")
    # print(new_string)
    return new_string

# 定义一个函数，接受一个字符串作为参数，返回替换后的字符串
def remove_space_after_decimal(s):
    # 定义一个正则表达式，匹配像 2. 4 和 1. 35 这样的小数
    pattern = r"\d+\.\s*\d+"
    # 定义一个回调函数，接受一个匹配对象作为参数，返回替换后的字符串
    def repl(m):
        # 从匹配对象中获取匹配的字符串
        num = m.group()
        # 去掉字符串中的空格
        num = num.replace(" ", "")
        # 返回去掉空格后的字符串
        return num
    # 使用 re.sub 函数，传入正则表达式，回调函数和原始字符串，进行替换操作
    return re.sub(pattern, repl, s)


#TAI SOU
# # 定义一个函数，输入一个句子列表，输出一个去掉单词数量小于4的句子的列表 Taisou
# def filter_sentences(sentences):
#     # 初始化一个空列表，用来存储过滤后的句子
#     print("----------过滤之前的数据----------",sentences)
#     filtered = []
#     # 遍历句子列表中的每个句子
#     for sentence in sentences:
#         # 使用 split 方法，将句子按空格分割成单词列表
#         words = sentence.split()
#         # seg_list = jieba.cut(sentence, cut_all=False)
#         # 如果单词列表的长度大于等于4，说明句子的单词数量不小于4，将句子加入到过滤后的列表中
#         if len(words) < 2 and len(re.findall('[\u4e00-\u9fa5]', sentence)) > 5:
#             filtered.append(sentence)
#     # 返回过滤后的句子列表
#     return filtered


#NASA
#  定义一个函数，输入一个句子列表，输出一个去掉单词数量小于4的句子的列表 NASA
def filter_sentences(sentences):
    # 初始化一个空列表，用来存储过滤后的句子
    print("----------过滤之前的数据----------",sentences)
    filtered = []
    # 遍历句子列表中的每个句子
    for sentence in sentences:
        # 使用 split 方法，将句子按空格分割成单词列表
        words = sentence.split()
        # seg_list = jieba.cut(sentence, cut_all=False)
        # 如果单词列表的长度大于等于4，说明句子的单词数量不小于4，将句子加入到过滤后的列表中
        if len(words) > 4:
            filtered.append(sentence)
    # 返回过滤后的句子列表
    return filtered




def file2textlist(filename,filepageone,filepagetwo):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_dir = BASE_DIR + '\\requirement\\'
    string_pdf = ''
    list_string_pdf = []
    with pdfplumber.open(path_dir+filename) as pdf:
         num_pages = len(pdf.pages)
         for page_num in range(filepageone,filepagetwo):
            page = pdf.pages[page_num]
            text = page.extract_text()
            string_pdf = string_pdf + text
            # print(text)
    string_pdf = replace_newline(string_pdf)
    list_string_pdf = find_sentences(string_pdf)
    list_string_pdf = filter_sentences(list_string_pdf)
    #print(list_string_pdf)
    # print('.\n'.join(list_string_pdf))
    return list_string_pdf
