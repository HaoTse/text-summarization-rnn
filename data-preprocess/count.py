import logging

def main():
    logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)

    content_file = 'content_broken'
    title_file = 'title_broken'

    with open(content_file, 'r', encoding='utf-8') as f:
        content_lines = f.readlines()
    with open(title_file, 'r', encoding='utf-8') as f:
        title_lines = f.readlines()
    
    if len(title_lines) != len(content_lines):
        logging.error('長度不相同')
        return
    total = len(title_lines) * 1.0

    content_len, title_len = 0.0, 0.0
    content_max, title_max = 0, 0
    content_min, title_min = 1000, 1000
    for i in range(round(total)):
        content_line = content_lines[i]
        title_line = title_lines[i]
        
        content_word = content_line.strip().split(" ")
        title_word = title_line.strip().split(" ")

        content_len += len(content_word) / total
        content_max = len(content_word) if len(content_word) > content_max else content_max
        content_min = len(content_word) if len(content_word) < content_min else content_min

        title_len += len(title_word) / total
        title_max = len(title_word) if len(title_word) > title_max else title_max
        title_min = len(title_word) if len(title_word) < title_min else title_min

        if not i % 10000:
            logging.info("Process %d lines" % i)

    logging.info("(average length, max length, min length) of content: (%.2f, %d, %d)" % (content_len, content_max, content_min))
    logging.info("(average length, max length, min length) of title: (%.2f, %d, %d)" % (title_len, title_max, title_min))

if __name__ == '__main__':
    main()