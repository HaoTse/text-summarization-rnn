# coding=utf-8

import jieba
import logging
import operator

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    title_file = 'title_broken_tmp_2'
    content_file = 'content_broken_tmp_2'

    # deal with title
    with open(title_file, 'r', encoding="utf-8") as f:
        title_lines = f.readlines()
    with open(content_file, 'r', encoding="utf-8") as f:
        content_lines = f.readlines()

    if len(title_lines) != len(content_lines):
        logging.error('長度不相同')

    voca = {}
    for i in range(len(title_lines)):
        title_line = title_lines[i]
        content_line = content_lines[i]

        for word in title_line.split(' '):
            if word in voca:
                voca[word] += 1
            else:
                voca[word] = 0
        for word in content_line.split(' '):
            if word in voca:
                voca[word] += 1
            else:
                voca[word] = 0
        if not (i % 10000):
            logging.info("已處理 %d 篇" % i)

    sort_voca = sorted(voca.items(), key=operator.itemgetter(1), reverse=True)
    # output vocabulary
    with open('voca', 'w', encoding="utf-8") as f:
        for word, times in sort_voca:
            f.write("%s %d\n" % (word, times))

    logging.info("vocabulary 大小為 %d", len(voca))


if __name__ == '__main__':
    main()