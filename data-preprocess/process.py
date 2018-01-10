import re

"""
First, must download the copus from SogouCS.
"""

def main():
    # "news_sohusite_xml.dat" is the file name download form SogouCS
    with open('news_sohusite_xml.dat', 'r', encoding="utf-8") as f:
        content = f.read()

    title_match = re.findall(r'<contenttitle>.*</contenttitle>', content)
    content_match = re.findall(r'<content>.*</content>', content)

    # empty file
    open('title', 'w').close()
    open('content', 'w').close()

    cnt = 0
    title = ''
    content = ''
    for t, c in zip(title_match, content_match):
        t = t.replace('<contenttitle>', '').replace('</contenttitle>', '')
        c = c.replace('<content>', '').replace('</content>', '')
        if not t or not c or t[-1] == '：':
            continue
        title += (t + '\n')
        content += (c + '\n')
        cnt += 1
        if not (cnt % 10000):
            with open('title', 'a', encoding="utf-8") as f:
                f.write(title)
            with open('content', 'a', encoding="utf-8") as f:
                f.write(content)
            title = ''
            content = ''

    with open('title', 'a', encoding="utf-8") as f:
        f.write(title)
    with open('content', 'a', encoding="utf-8") as f:
        f.write(content)
    print ("Total number: %d" % cnt)

if __name__ == '__main__':
    main()
