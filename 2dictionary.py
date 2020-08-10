#!/usr/bin/env python
# encoding: utf-8
"""

@Desc：采用python字典来表示每位用户评论的电影和评分
"""
file = open("data.csv", 'r', encoding='UTF-8')  # 记得读取文件时加‘r’， encoding='UTF-8'
##读取data.csv中每行中除了名字的数据
data = {}  ##存放每位用户评论的电影和评分
for line in file.readlines():
    # 注意这里不是readline()
    line = line.strip().split(',')
    # 如果字典中没有某位用户，则使用用户ID来创建这位用户
    if not line[0] in data.keys():
        data[line[0]] = {line[3]: line[1]}
    # 否则直接添加以该用户ID为key字典中
    else:
        data[line[0]][line[3]] = line[1]

#print(data)

from math import *
def Euclidean(user1, user2):
    # 取出两位用户评论过的电影和评分
    user1_data = data[user1]
    user2_data = data[user2]
    distance = 0
    # 找到两位用户都评论过的电影，并计算欧式距离
    for key in user1_data.keys():#用户1评分的所有电影
        if key in user2_data.keys():
            # 注意，distance越大表示两者越相似
            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)
    return 1 / (1 + sqrt(distance))  # 这里返回值越小，相似度越大


# 计算某个用户与其他用户的相似度
def top10_simliar(userID):
    res = []
    for userid in data.keys():
        # 排除与自己计算相似度
        if not userid == userID:
            simliar = Euclidean(userID, userid)
            res.append((userid, simliar))
    res.sort(key=lambda val: val[1])
    return res[:4]


RES = top10_simliar('3')
#print(RES)
#皮尔森相似度
def pearson_sim(user1, user2):
    # 取出两位用户评论过的电影和评分
    user1_data = data[user1]
    user2_data = data[user2]
    distance = 0
    common = {}

    # 找到两位用户都评论过的电影
    for key in user1_data.keys():
        if key in user2_data.keys():
            common[key] = 1
    if len(common) == 0:
        return 0  # 如果没有共同评论过的电影，则返回0
    n = len(common)  # 共同电影数目
    #print(n, common)
##计算评分和
    sum1 = sum([float(user1_data[movie]) for movie in common])
    sum2 = sum([float(user2_data[movie]) for movie in common])
    ##计算评分平方和
    sum1Sq = sum([pow(float(user1_data[movie]), 2) for movie in common])
    sum2Sq = sum([pow(float(user2_data[movie]), 2) for movie in common])
    ##计算乘积和
    PSum = sum([float(user1_data[it]) * float(user2_data[it]) for it in common])

    ##计算相关系数
    num = PSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    r = num / den
    return r
print('皮尔森')
R = pearson_sim('1', '3')
print(R)
def top_sim(userID):
    sim_rank=[]
    #print(type(data.keys()))
    for user in data.keys():
        if not user==str(userID) and user!='userId':
            sim_rank.append((user,pearson_sim(str(userID),user)))#将评分和对应相似用户存入rank中
    sim_rank.sort(key=lambda val: val[1])#按照列表中的第2个元素排序
    return sim_rank[:5]

print("jjj")
#print(top_sim(3))

########################################################################
# 根据用户推荐电影给其他人
def recommend(user):
    # 相似度最高的用户,两种找相似度的方式
    top_sim_user1 = top10_simliar(user)[0][0]
    top_sim_user=top_sim(user)[0][0]
    # 相似度最高的用户的观影记录
    items1 = data[top_sim_user1]
    items = data[top_sim_user]
    recommendations = []
    recommendations1 = []
    # 筛选出该用户未观看的电影并添加到列表中
    for item in items.keys():
        if item not in data[user].keys():
            recommendations.append((item, items[item]))
    recommendations.sort(key=lambda val: val[1], reverse=True)  # 按照评分排序
    # 返回评分最高的10部电影
    for item in items1.keys():
        if item not in data[user].keys():
            recommendations1.append((item, items1[item]))
    recommendations1.sort(key=lambda val: val[1], reverse=True)  # 按照评分排序
    # 返回评分最高的10部电影
    print(recommendations[:10])
    print(recommendations1[:10])
    return

Recommendations = recommend('1')
