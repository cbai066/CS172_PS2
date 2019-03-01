from math import *
from docIndex import *
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import string

ps = PorterStemmer()


def tf_idf_q(postings_doc, doc_index, postings_query, query_index):
    tf = []
    idf = []
    tf_idf_temp = []
    tf_idf_query = []
    ids = []
    count_terms = 0  # count the number of terms in the query
    count_doc = 0  # count the number of doc in which term occurs

    for posting_doc in postings_doc:
        count_doc += 1
    # print(count_doc)

    for posting_query in postings_query:
        count_terms = query_index[posting_query[0]]
        # print(count_terms)
        tf.append(round(posting_query[1], 8) / round(count_terms, 8))
        ids.append(posting_query[0])
        # print(round(posting_doc[1], 8) / round(count_terms, 8))
        idf.append(log2(len(doc_index) / count_doc))

    tf_idf_temp = [a * b for a, b in zip(tf, idf)]
    for i in range(len(ids)):
        tf_idf_query.append([ids[i], tf_idf_temp[i]])
    return tf_idf_query


def tf_idf_d(postings, doc_index):
    tf_idf_doc = []
    count_terms = 0  # count the number of terms in the doc
    count_doc = 0  # count the number of doc in which term occurs

    for posting in postings:
        count_doc += 1
    # print(count_doc)
    for posting in postings:
        count_terms = doc_index[posting[0]]
        # print(count_terms)
        tf = round(posting[1], 8) / round(count_terms, 8)
        # print(round(posting[1], 8) / round(count_terms, 8))
        idf = log(len(doc_index) / count_doc)
        tf_idf_doc.append([posting[0], tf * idf])

    return tf_idf_doc


def CosineScore():
    #file1 = "data2/ap89_collection"
    file_d = input("Please enter an absolute file path to doc you wanna search ")
    (terms_d, postings_d, numDocs_d, docIndex_d, docNum_d, postings_wd) = docRetrieval(file_d)

    #file2 = "data2/query_list.txt"
    file_q = input("Please enter an absolute file path to the query ")
    (terms_q, postings_q, numDocs_q, queryIndex_q, queryNum_q, postings_wq) = queryRetrieval(file_q)

    score = {key: 0 for key in docIndex_d}
    length_d = {}
    length_q = {}
    weights_d = {key: [] for key in docIndex_d}
    weights_q = {key: [] for key in queryIndex_q}

    for term_d in terms_d:
        array = tf_idf_d(postings_d[term_d], docIndex_d)
        for i in range(len(array)):
            weights_d[array[i][0]].append([term_d, array[i][1]])

    for term_q in terms_q:
        if term_q in terms_d:
            array = tf_idf_q(postings_d[term_q], docIndex_d, postings_q[term_q], queryIndex_q)
            for i in range(len(array)):
                weights_q[array[i][0]].append([term_q, array[i][1]])
        else:
            for array in postings_q[term_q]:
                weights_q[array[0]].append([term_q, 0])

    for id_d in weights_d:
        s = 0
        for i in range(len(weights_d[id_d])):
            s += pow(weights_d[id_d][i][1], 2)
        length_d[id_d] = sqrt(s)

    for id_q in weights_q:
        s = 0
        for i in range(len(weights_q[id_q])):
            s += pow(weights_q[id_q][i][1], 2)
        length_q[id_q] = sqrt(s)

    fp = open('data2/results_file.txt', 'w+')

    for index_q in queryIndex_q:
        for index_d in docIndex_d:
            for term_q in postings_wq[index_q]:
                if term_q in postings_wd[index_d]:
                    for i in range(len(weights_q[index_q])):
                        if weights_q[index_q][i][0] == term_q:
                            weight_q = weights_q[index_q][i][1]
                    for j in range(len(weights_d[index_d])):
                        if weights_d[index_d][j][0] == term_q:
                            weight_d = weights_d[index_d][j][1]
                    score[index_d] = score[index_d] + weight_d * weight_q
            score[index_d] = score[index_d] / (length_d[index_d] * length_q[index_q])
        score = collections.OrderedDict(sorted(score.items(), reverse=True, key=lambda t: t[1]))
        i = 0
        for DocNO in score:
            i += 1
            if score[DocNO] != 0:
                fp.write('{query_number} Q0 {DocNO} {rank} {score} Exp\n'.format(query_number=index_q, DocNO=DocNO, rank=i,
                                                                        score=score[DocNO]))
                print('{query_number} Q0 {DocNO} {rank} {score} Exp'.format(query_number=index_q, DocNO=DocNO, rank=i,
                                                                        score=score[DocNO]))
        score = {key: 0 for key in docIndex_d}



if __name__ == "__main__":
    CosineScore()
