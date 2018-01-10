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
def SeqSentence(s, mode = ''):
    s = FullToHalf(s)
    s = process(s)
    s = jieba.cut(s.strip(), cut_all=False)
    outstr = ''
    cnt = 0
    for word in s:
        if (mode == 'title' and cnt > 30) or (mode == 'content' and cnt > 120):
            break
        if word not in stopwords and word != '\t' and word != ' ' and word != '\ue40c':
            outstr += (word + ' ')
            if word not in voca:
                voca.append(word)
            cnt += 1
    return outstr + '\n'

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # empty file
    open('title_broken', 'w').close()
    open('content_broken', 'w').close()
    
    # deal with title
    with open('title', 'r', encoding="utf-8") as f:
        content = f.readlines()

    output = ''
    cnt = 0
    for line in content:
        words = SeqSentence(line, 'title')
        output += (words)
        cnt += 1
        if not (cnt % 10000):
            logging.info("已處理 %d 篇title" % cnt)
            with open('title_broken', 'a', encoding="utf-8") as f:
                f.write(output)
            output = ''
    title_num = cnt
    with open('title_broken', 'a', encoding="utf-8") as f:
        f.write(output)

    # deal with content
    with open('content', 'r', encoding="utf-8") as f:
        content = f.readlines()

    output = ''
    cnt = 0
    for line in content:
        words = SeqSentence(line, 'content')
        output += (words)
        cnt += 1
        if not (cnt % 10000):
            logging.info("已處理 %d 篇content" % cnt)
            with open('content_broken', 'a', encoding="utf-8") as f:
                f.write(output)
            output = ''
    content_num = cnt
    with open('content_broken', 'a', encoding="utf-8") as f:
        f.write(output)
    
    # output vocabulary
    with open('voca', 'w', encoding="utf-8") as f:
        for word in voca:
            f.write("%s\n" % word)
    
    logging.info("共處理 (%d, %d) 篇", title_num, content_num)
    logging.info("vocabulary 大小為 %d", len(voca))

if __name__ == '__main__':
    main()