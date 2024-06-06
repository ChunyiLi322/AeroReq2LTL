# 导入所需的库
import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 定义一个函数，用来去掉矩阵的对角线元素
def remove_diagonal(matrix):
  # 获取矩阵的形状
  rows, cols = matrix.shape
  # 创建一个新的矩阵，用来存储去掉对角线元素后的结果
  new_matrix = np.zeros((rows, cols - 1))
  # 遍历每一行
  for i in range(rows):
    # 将对角线元素左边的元素复制到新矩阵
    new_matrix[i, :i] = matrix[i, :i]
    # 将对角线元素右边的元素复制到新矩阵
    new_matrix[i, i:] = matrix[i, i + 1:]
  # 返回新矩阵
  return new_matrix

# 定义一个函数，用来计算矩阵的平均值
def matrix_mean(matrix):
  # 使用numpy的mean函数，对矩阵的所有元素求平均值
  return np.mean(matrix)

def compute_sim(sentences):
    # # 定义四个中文句子
    # sentences = ["我喜欢吃苹果", "苹果是一种水果", "我不喜欢吃香蕉", "香蕉有很多营养"]

    if len(sentences)<2:
        return 1;

    # 对句子进行分词
    words = []
    for sentence in sentences:
        words.append(" ".join(jieba.cut(sentence)))

    # 将分词后的句子转换为TF-IDF向量
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(words)

    # 计算向量之间的余弦相似度
    similarity = cosine_similarity(vectors)

    # 将相似度的结果保存到矩阵中
    matrix = np.array(similarity)
    mean = np.mean(matrix)
    # 打印矩阵
    # print(mean)
    # 调用函数，得到去掉对角线元素后的矩阵
    new_matrix = remove_diagonal(matrix)
    # 调用函数，得到矩阵的平均值
    mean = matrix_mean(new_matrix)
    # 打印结果，保留两位小数
    # print(mean)
    return mean



