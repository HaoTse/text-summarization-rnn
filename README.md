# text-summarization

## Prepare in advance

### Environment
This version is constructed on tensorflow1.0 and pyton2.7.
- The command to install tensorflow1.0 in ubuntu 
```
pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.0.0-cp27-none-linux_x86_64.whl
```

### Download corpus
1. download from [SogouCS](http://www.sogou.com/labs/resource/cs.php).
2. Put the corpus in `data-preprocess/` folder.

## Data preprocessing
```
.
├── process.py
├── broken.py
├── count.py
├── vocabulary.py
└── src/
```

1. After download corpus, run the `process.py`. And it will deal the corpus to find content and title.
2. It will generate `content` and `title`.
3. Run `broken.py`, it will use jieba to segment cotent and title. And this will generate `content_broken` and `title_broken`.
4. Run `count.py`, it can count the segment words length of file, and can use the result to define bucket.
5. Run `vocabulary.py`, it can output the vocabulary of all content and title.
