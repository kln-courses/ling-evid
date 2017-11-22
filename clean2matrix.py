#!/home/kln/anaconda2/bin/python
# -*- coding: utf-8 -*-
"""
export preprocessed documents to matrix using standard preprocessing for NLP tasks
usage: $./clean2matrix.py /home/kln/Documents/edu/hist_03/data

"""
import glob, os, re, sys, textmining
from nltk.corpus import wordnet
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

def read_txt(path):
    fnames = sorted(glob.glob(os.path.join(path,"*.txt")))
    data = []
    metadata = []
    for fname in fnames:
        with open(fname, 'r') as f:
            data.append(f.read())
        metadata.append(os.path.basename(fname).split(".")[0])
    return data, metadata

def clean(s):
    return re.sub(r"\d","",s.lower())

def tokenize(s, n = 1):
    """
    n-gram tokenization of string with maximum overlap
    """
    if type(s) == unicode:
        tokenizer = re.compile(r'\W*', re.UNICODE)
    else:
        tokenizer = re.compile(r'\W*')
    unigram = tokenizer.split(s)
    if n > 1:
        return [unigram[i:i+n] for i in range(len(unigram)-(n-1))]
    else:
        return [s for s in unigram if s]

def stopfilter(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if token not in stopwords.words('english')]
    tokens = [token for token in tokens if len(token) > 1]
    return " ".join(tokens)

def treebank2wordnet(treebank_tag):
    """
    map treebank pos tags to wordnets four categories:
    - n: noun (default), v: verb, a: adjective, and r: adverbs
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN# noun is baseline

def pos_sensitive_lemmatizer(text):
    """
    lemmatizer with treebank pos tags
    - string as in- and output
    """
    tokens = tokenize(text)
    tokens_tag = pos_tag(tokens, tagset = 'universal', lang = 'eng')
    lemmatizer = WordNetLemmatizer()
    output = []
    for i in range(len(tokens_tag)):
        output.append(lemmatizer.lemmatize(tokens_tag[i][0],
        treebank2wordnet(tokens_tag[i][1])))
    return " ".join(output)

def texts2matrix(texts, titles, fname = 'dtm.csv'):
    M = textmining.TermDocumentMatrix()
    for text in texts:
        M.add_doc(text)
    M.write_csv(fname, cutoff=3)
    tname = fname.split('.')[0] + '_filename.txt'
    f = open(tname, 'w')
    for i in titles:
      f.write("%s\n" % i)
    print "matrix saved as " + fname + " and filenames as " + tname

def main():
    #dpath = "/home/kln/Documents/edu/hist_03/data"
    dpath = sys.argv[1]
    texts, titles = read_txt(dpath)
    texts = map(clean,texts)
    texts = map(stopfilter, texts)
    texts = map(pos_sensitive_lemmatizer, texts)
    texts2matrix(texts, titles)

if __name__ == '__main__':
    main()
