from collections import Counter

from bs4 import BeautifulSoup
from nltk import clean_html
from nltk import data
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import treebank
from numpy import array
from requests import get

import testextract
import wiki2plain


class Edge(object):
    head = None
    tail = None
    weight = None

    def __init__(self, head, tail, weight):
        self.head = head
        self.tail = tail
        self.weight = weight

    def __repr__(self):
        return unicode(self)

    def __unicode__(self):
        return u'Edge from <%s> to <%s> with weight %f' % (unicode(self.head),
                                                           unicode(self.tail),
                                                           self.weight,)


class Node(object):
    value = None
    entering_edges = None
    exiting_edges= None

    def __init__(self, value, entering_edges=None, exiting_edges=None):
        self.value = value
        self.entering_edges = entering_edges or set()
        self.exiting_edges = exiting_edges or set()

    def __repr__(self):
        return unicode(self)

    def __unicode__(self):
        return u'Node with value "%s"' % unicode(self.value)

    def connect(self, node, weight):
        edge = Edge(self, node, weight)
        self.exiting_edges.add(edge)
        node.entering_edges.add(edge)

    def get_all_edges(self):
        return self.entering_edges | self.exiting_edges

    def get_neighbors(self):
        edges = self.get_all_edges()
        nodes = set([edge.head for edge in edges]) | set([edge.tail for edge in edges])
        nodes.remove(self)
        return nodes

    def get_edge(self, node):
        for edge in self.get_all_edges():
            if ((edge.head == self and edge.tail == node) or
                    (edge.head == node and edge.tail == self)):
                return edge
        return None


def cosine_distance(sentence1, sentence2, naive=True):
    stopwords_set = set(stopwords.words())
    def make_counter(sentence):
        words = word_tokenize(sentence)[:-1]
        words = filter(lambda word: word not in stopwords_set, words)

        return Counter(words)
    def length(vector):
        return sum((item ** 2 for item in vector)) ** 0.5

    if not naive:
        raise NotImplementedError()

    words1, words2 = make_counter(sentence1), make_counter(sentence2)

    common_words = set(words1.keys()) & set(words2.keys())
    numerator = sum([words1[word] ** 2 * words2[word] ** 2 for word in common_words])
    denom = length(words1.values()) * length(words2.values())

    if not denom:
        return 0.0
    else:
        return numerator / denom


def construct_graph(document):
    sentence_detector = data.load('tokenizers/punkt/english.pickle')
    sentences = sentence_detector.tokenize(document)

    nodes = [Node(sentence) for sentence in sentences]
    for idx1 in range(len(nodes)):
        print idx1, len(nodes)
        for idx2 in range(idx1 + 1, len(nodes)):
            node1, node2 = nodes[idx1], nodes[idx2]
            edge_weight = cosine_distance(node1.value, node2.value)
            node1.connect(node2, edge_weight)

    return nodes

    
def page_rank(graph, iterations=10, dampening=0.85):
    page_ranks = {}
    num_nodes = len(graph)

    for _ in range(iterations):
        if _ != (iterations - 1):
            print _
        else:
            print "BLASTOFF"
        new_page_ranks = {}
        for node in graph:
            neighbors = node.get_neighbors()
            new_page_rank = 0
            for neighbor in neighbors:
                weighted_neighbor_deg = sum([edge.weight for edge in neighbor.get_all_edges()])
                if weighted_neighbor_deg != 0:
                    edge = node.get_edge(neighbor)
                    new_page_rank += edge.weight * page_ranks.get(neighbor, 1) / weighted_neighbor_deg
            new_page_rank = (1-dampening) / len(graph) + dampening * new_page_rank
            new_page_ranks[node] = new_page_rank
        page_ranks = new_page_ranks.copy()

    return page_ranks


def get_central_nodes(page_rank_result, k):
    node_list = [node for node in page_rank_result.iterkeys()]
    node_list.sort(key=lambda x:page_rank_result[x], reverse=True)
    return node_list[:k]
    
if __name__ == '__main__':
    '''
    url = raw_input('URL?\n')
    response = get(url)
    soup = BeautifulSoup(response.content)
    text = soup.find('div', {'id': 'mw-content-text'}).text
    text = text.encode('ascii', 'ignore')
    '''
    #print text
    #text = '  '.join([line for line in open('test2.txt').readlines()])
    article_name = raw_input('Article?\n')
    lang = 'en'
    wiki = testextract.Wikipedia(lang)

    try:
        raw = wiki.article(article_name)
    except:
        raw = None

    if raw:
        wiki2plain = wiki2plain.Wiki2Plain(raw)
        content = wiki2plain.text
    graph = construct_graph(content)
    page_rank_result = page_rank(graph)
    central_nodes =  get_central_nodes(page_rank_result, 3)
    for node in central_nodes:
        print node.value, '\n'

