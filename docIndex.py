import os
import xml.etree.ElementTree as ElementTree
import string

from nltk import collections
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()

translator = str.maketrans('', '', string.punctuation)


def getDocID(file):
    (doc_id, extension) = os.path.splitext(file)
    doc_id = int(doc_id[4:6])
    return doc_id


def getDocInfo(file):
    with open(file, 'r') as f:  # Reading file
        xml = f.read()

    xml = '<ROOT>' + xml + '</ROOT>'  # Let's add a root tag

    root = ElementTree.fromstring(xml)

    docs = []

    for doc in root:
        docs.append([doc.find('DOCNO').text.strip(), doc.find('TEXT').text.strip()])

    return docs


# file = "data2/query_list.txt"
def getQuery(file):
    nums = []
    queries = []

    f = open(file, 'r+')

    for line in f.readlines():
        line = line.strip().translate(translator)
        a = line.split()

        #obtain the query-number in the file
        num = int(a[0])
        nums.append(num)

        #obtain the query-text in the file
        query = line.strip(a[0]).strip()
        queries.append([num, query])

    return queries


'''
def queryFreq(query, term):
    freq = 0
    for term in query[1].split():
        freq += 1
    return freq
'''


def queryRetrieval(file):
    stop_words = set(open("stoplist.txt").read().split("\n"))

    # file = "data2/query_list.txt"
    files = getQuery(file)
    query_ids = []
    for file in files:
        query_id = file[0]
        query_ids.append(query_id)

    queryIndex = {docID: 0 for docID in query_ids}
    # query_id: the number of terms in that document

    postings_words = {}

    terms = set([])
    # search all the terms
    for file in files:
        query_id = file[0]
        new_text = file[1].translate(translator)
        temp_words = word_tokenize(new_text)
        for n, i in enumerate(temp_words):
            temp_words[n] = i.lower()
            temp_words[n] = ps.stem(i)
        temp_terms = set(temp_words)
        temp_terms -= stop_words
        queryIndex[query_id] = len(temp_terms)
        terms = terms | temp_terms
        postings_words[query_id] = temp_terms

    queryIndex = collections.OrderedDict(sorted(queryIndex.items(), key=lambda t: t[0]))
    postings = {term: [[0, 0] for i in range(len(query_ids))] for term in terms}
    # form of posting: {term1:[[docID1,docFreq1],[docID2,docFreq2],...],}
    numQuery = {term: 0 for term in terms}
    # form of numDocs: {term: the number of documents that contain the term}

    queryNum = 0

    for file in files:
        query_id = file[0]
        words = word_tokenize(file[1].translate(translator))
        for n, i in enumerate(words):
            words[n] = i.lower()
            words[n] = ps.stem(i)
        for word in words:
            if word not in stop_words:
                postings[word][queryNum][0] = query_id
                postings[word][queryNum][1] += 1
        queryNum += 1

    for term in terms:
        new_postings = []
        for posting in postings[term]:
            if not posting[1] == 0:
                new_postings.append(posting)
        postings[term] = new_postings
        numQuery[term] = len(new_postings)

    postings = collections.OrderedDict(sorted(postings.items(), key=lambda t: t[0]))

    return terms, postings, numQuery, queryIndex, queryNum, postings_words


def docRetrieval(file_path):
    stop_words = set(open("stoplist.txt").read().split("\n"))

    # file = "data2/ap89_collection"
    files = getDocInfo(file_path)
    doc_ids = []
    for file in files:
        doc_id = file[0]
        doc_ids.append(doc_id)

    docIndex = {docID: 0 for docID in doc_ids}
    # doc_id: the number of terms in that document

    postings_words = {}

    terms = set([])
    # search all the terms
    for file in files:
        doc_id = file[0]
        new_text = file[1].translate(translator)
        temp_words = word_tokenize(new_text)
        for n, i in enumerate(temp_words):
            temp_words[n] = i.lower()
            temp_words[n] = ps.stem(i)
        temp_terms = set(temp_words)
        temp_terms -= stop_words
        docIndex[doc_id] = len(temp_terms)
        terms = terms | temp_terms
        postings_words[doc_id] = temp_terms

    postings = {term: [[0, 0] for i in range(len(doc_ids))] for term in terms}
    # form of posting: {term1:[[docID1,docFreq1],[docID2,docFreq2],...],}
    numDocs = {term: 0 for term in terms}
    # form of numDocs: {term: the number of documents that contain the term}

    docNum = 0

    for file in files:
        doc_id = file[0]
        words = word_tokenize(file[1].translate(translator))
        for n, i in enumerate(words):
            words[n] = i.lower()
            words[n] = ps.stem(i)
        for word in words:
            if word not in stop_words:
                postings[word][docNum][0] = doc_id
                postings[word][docNum][1] += 1
        docNum += 1

    for term in terms:
        new_postings = []
        for posting in postings[term]:
            if not posting[1] == 0:
                new_postings.append(posting)
        postings[term] = new_postings
        numDocs[term] = len(new_postings)

    postings = collections.OrderedDict(sorted(postings.items(), key=lambda t: t[0]))

    return terms, postings, numDocs, docIndex, docNum, postings_words


def docIndex(path):
    stop_words = set(open("stoplist.txt").read().split("\n"))

    # path = "/Users/27422/PycharmProjects/HW/data1"
    files = os.listdir(path)
    doc_ids = []
    for file in files:
        doc_id = getDocID(file)
        doc_ids.append(doc_id)

    docIndex = {docID: 0 for docID in doc_ids}
    # doc_id: the number of terms in that document

    terms = set([])
    # search all the terms
    for file in files:
        if not os.path.isdir(file):
            doc_id = getDocID(file)
            temp = open(path + '/' + file).read().split(" ")
            for n, i in enumerate(temp):
                temp[n] = i.lower()
            temp_terms = set(temp)
            temp_terms -= stop_words
            docIndex[doc_id] = len(temp_terms)
            terms = terms | temp_terms

    postings = {term: [[0, 0] for i in range(len(doc_ids))] for term in terms}
    # form of posting: {term1:[[docID1,docFreq1],[docID2,docFreq2],...],}
    numDocs = {term: 0 for term in terms}
    # form of numDocs: {term: the number of documents that contain the term}

    for file in files:
        if not os.path.isdir(file):
            doc_id = getDocID(file)
            words = open(path + '/' + file).read().split(" ")
            for n, i in enumerate(words):
                words[n] = i.lower()
            for word in words:
                if word not in stop_words:
                    postings[word][doc_id - 1][0] = doc_id
                    postings[word][doc_id - 1][1] += 1

    for term in terms:
        new_postings = []
        for posting in postings[term]:
            if not posting[1] == 0:
                new_postings.append(posting)
        postings[term] = new_postings
        numDocs[term] = len(new_postings)

    return terms, postings, numDocs, docIndex
