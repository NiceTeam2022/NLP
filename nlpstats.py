# # 功能说明
# 
# 中文文本的指标计算。
# 
# - **平均句长：** 分句后，各句子字数的平均值。
# 
# - **信息密度：** 实词词汇密度，即非停用词的占所有词数的比值。
# 
# - **情感：** 根据情感词典计算出的情感两级分类、情感极性（积极/消极程度）、情感强度（强烈程度）。

import re
import numpy as np
import jieba


# 本地使用，之后需要删除
import pandas as pd
sentiment_dict = pd.read_excel('情感词汇本体.xlsx')
sentiment_dict


# 分句符号
# 来源zhon.hanzi.sentence
sentence_sign = '[〇一-\u9fff㐀-\u4dbf豈-\ufaff𠀀-\U0002a6df𪜀-\U0002b73f𫝀-\U0002b81f丽-\U0002fa1f⼀-⿕⺀-⻳＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·]*[！？｡。][」﹂”』’》）］｝〕〗〙〛〉】]*'

# 停用词表
with open('哈工大中文停用词表.txt', 'r', encoding='utf-8') as f:
    stopwords = f.readlines()


# Broadcasting计算长度
nplen = np.frompyfunc(len, 1, 1)

# 平均句长
def avg_sent_len(text): 
    # 删除英文
    text_ = re.sub('[a-zA-Z]', '', text_)
    # 分段
    paras = text_.split('\n')
    sents = []
    for para in paras:
        # 分句
        # 注：会忽略含英文的句子
        sents += re.findall(sentence_sign, para)
    # 保留汉字
    sents_de_punc = []
    for sent in sents:
        sents_de_punc += [re.sub('[^\u4e00-\u9fff]*', '', sent)]
    
    return nplen(sents_de_punc).mean()


# 信息密度
# 以下算法在已测试算法中效率最高
def info_den(text):
    # 删除英文
    text_ = re.sub('[a-zA-Z]', '', text_)
    # 分词
    words = jieba.lcut(text_)
    # 实词（非停用词）
    notions = list(filter(lambda x: False if x in stopwords else True, words))
    
    return len(notions) / len(words)


# 情感
def sentiment(text):
    pass