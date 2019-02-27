from math import *
from docIndex import *
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import string
ps = PorterStemmer()


def tf_idf_q(postings, doc_index, query, term):
    tf = []
    idf = []
    tf_idf = []
    count_terms = 0  # count the number of terms in the doc
    count_doc = 0  # count the number of doc in which term occurs

    for posting in postings:
        count_doc += 1
    print(count_doc)
    for posting in postings:
        count_terms = doc_index[posting[0]]
        # print(count_terms)
        tf.append(round(queryFreq(query, term), 8) / round(count_terms, 8))
        # print(round(posting[1], 8) / round(count_terms, 8))
        idf.append(log2(len(doc_index) / count_doc))

    tf_idf = [a * b for a, b in zip(tf, idf)]
    return tf_idf


def tf_idf(postings, doc_index):
    tf = []
    idf = []
    tf_idf = []
    count_terms = 0  # count the number of terms in the doc
    count_doc = 0  # count the number of doc in which term occurs

    for posting in postings:
        count_doc += 1
    print(count_doc)
    for posting in postings:
        count_terms = doc_index[posting[0]]
        # print(count_terms)
        tf.append(round(posting[1], 8) / round(count_terms, 8))
        # print(round(posting[1], 8) / round(count_terms, 8))
        idf.append(log(len(doc_index) / count_doc))

    tf_idf = [a * b for a, b in zip(tf, idf)]
    return tf_idf


def CosineScore(query, postings,terms):
    score = 0
    length = 0

    file =  input("Please enter an abosolute file path to ")
    weights_p = {}
    for query in getQuery(file):
        temp_words = word_tokenize(query)
        for n, i in enumerate(temp_words):
            temp_words[n] = i.lower()
            temp_words[n] = ps.stem(i)

        for term in terms:

    '''
    for i in range(len(postings)):
        print(f"result in document file{postings[i][0]:d}: tf:{tf[i]:f}; idf:{idf[i]:f}; tf-idf:{tf_idf[i]:f}")
    '''


# path = "/Users/27422/PycharmProjects/HW/data"
'''
path = input("Enter an absolute path to data")
(terms, postings, numDocs, docIndex) = docIndex(path)
'''

if __name__ == "__main__":
    '''
    while (1):
        term = input("Enter a term: (Enter QUIT for termination) ")
        if term == 'QUIT':
            break
        if term in terms:
            print(postings[term])
            tf_idf(postings[term], numDocs[term], docIndex)
        if term not in terms:
            print("\'%s\' does not appear in the collections. Please re-enter a term" % term)
    
    for i in getDocInfo(file="/Users/27422/PycharmProjects/HW/data2/ap89_collection"):
        print(i)

    new_text = "It is important to by very pythonly while you are pythoning with python. All pythoners have pythoned poorly at least once."
    words = word_tokenize(new_text)
    print(words)

    for w in words:
        print(ps.stem(w))
   print(getQuery('data2/query_list.txt'))
'''
    path = "data2/ap89_collection"
    print(docRetrieval(path))

