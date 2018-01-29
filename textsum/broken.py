# coding=utf-8

import jieba
import re
import logging
import io

# load zh-TW dictionary
jieba.set_dictionary('../data-preprocess/src/dict.txt.big')

# transfer full-shape to half-shape
def FullToHalf(s):
    n = []
    for char in s:
        num = ord(char)
        if num == 0x3000:
            num = 32
        elif 0xFF01 <= num <= 0xFF5E:
            num -= 0xfee0
        num = chr(num)
        n.append(num)
    return ''.join(n)

# load stopwords
with io.open('../data-preprocess/src/stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = [line.strip() for line in f.readlines()]

# initial vocabulary
voca = ['_PAD', '_GO', '_EOS', '_UNK']

# preprocess the file content
def process(s):
    # YYYY年MM月[DD日]
    s = re.sub(r'(19|20)?[0-9]{2}[- /.\u5e74](0?[1-9]|1[012])[- /.\u6708]((0?[1-9]|[12][0-9]|3[01])\u65e5)?', 'TAG_DATE', s)
    # MM月DD日
    s = re.sub(r'(0?[1-9]|1[012])[- /.\u6708](0?[1-9]|[12][0-9]|3[01])\u65e5', 'TAG_DATE', s)
    # number, decimal and percent
    s = re.sub(r'[0-9]+(.?[0-9]+)?%?', 'TAG_NUM', s)
    return s

# sqgment the input
def SeqSentence(sentence):
    sentence = FullToHalf(sentence)
    sentence = process(sentence)
    sentence = jieba.cut(sentence.strip(), cut_all=False)

    sentence_list = []

    for word in sentence:
        if word not in stopwords and word != '\t' and word != ' ' and word != '\ue40c':
            sentence_list.append(word)

    sentence_str = ' '.join(sentence_list)
    return sentence_str
