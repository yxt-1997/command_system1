#通过如下程序提取数据：
# !/usr/bin/env python
# encoding: utf-8
"""
@Desc：读取用户的电影数据和评分数据
"""
import pandas as pd
movies = pd.read_csv("E:\python项目集合\知识图谱\推荐系统\ml-latest-small\movies.csv")
ratings = pd.read_csv("mratings.csv")  ##这里注意如果路径的中文件名开头是r，要转义。
data = pd.merge(movies, ratings, on='movieId')  # 通过两数据框之间的movieId连接
data[['userId', 'rating', 'movieId', 'title']].sort_values('userId').to_csv(
    'data.csv', index=False)