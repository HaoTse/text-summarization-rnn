# coding=utf-8

import jieba
import re
import logging

# load zh-TW dictionary
jieba.set_dictionary('src/dict.txt.big')

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
with open('src/stopwords.txt', 'r', encoding='utf-8') as f:
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
def SeqSentence(title, content):
    title = FullToHalf(title)
    title = process(title)
    title = jieba.cut(title.strip(), cut_all=False)

    content = FullToHalf(content)
    content = process(content)
    content = jieba.cut(content.strip(), cut_all=False)

    title_list, content_list = [], []

    for word in content:
        if word not in stopwords and word != '\t' and word != ' ' and word != '\ue40c':
            content_list.append(word)

    if len(content_list) > 250 or len(content_list) < 30:
        return None, None

    for word in title:
        if word not in stopwords and word != '\t' and word != ' ' and word != '\ue40c':
            title_list.append(word)

    if len(title_list) < 5:
        return None, None

    title_str = ' '.join(title_list) + '\n'
    content_str = ' '.join(content_list) + '\n'
    return title_str, content_str

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    title_file = 'title_broken_ori'
    content_file = 'content_broken_ori'

    # empty file
    open(title_file, 'w').close()
    open(content_file, 'w').close()
    
    # deal with title
    with open('title', 'r', encoding="utf-8") as f:
        title_lines = f.readlines()
    with open('content', 'r', encoding="utf-8") as f:
        content_lines = f.readlines()

    if len(title_lines) != len(content_lines):
        logging.error('長度不相同')

    title_output, content_output = '', ''
    cnt = 0
    for i in range(len(title_lines)):
        title_line = title_lines[i]
        content_line = content_lines[i]

        if '產品名稱' in content_line or '常見問題' in content_line or '綜合評價' in content_line:
            continue

        title_str, content_str = SeqSentence(title_line, content_line)
        
        if not title_str or not content_str:
            continue

        title_output += (title_str)
        content_output += (content_str)
        cnt += 1
        if not (cnt % 10000):
            logging.info("已處理 %d 篇" % cnt)
            with open(title_file, 'a', encoding="utf-8") as f:
                f.write(title_output)
            title_output = ''
            with open(content_file, 'a', encoding="utf-8") as f:
                f.write(content_output)
            content_output = ''

    with open(title_file, 'a', encoding="utf-8") as f:
        f.write(title_output)
    with open(content_file, 'a', encoding="utf-8") as f:
        f.write(content_output)
    
    logging.info("共處理 %d 篇", cnt)

if __name__ == '__main__':
    main()