from collections import Counter
from random import shuffle
from re import match

from nltk.corpus import treebank
from nltk.tree import Tree


productions = {}
tags = set()

class Production(object):
    variable = None
    expansion = None

    def __init__(self, variable):
        self.variable = variable
        self.expansion = Counter()

    def add(self, expansion):
        self.expansion[expansion] += 1

    def to_string(self):
        template = '%s -> %s'
        tot_count = 0
        for key, val in self.expansion.iteritems():
            if key:
                tot_count += val
        total = 0
        for key, val in self.expansion.iteritems():
            if key:
                total += float('%f' % (float(val) / tot_count))
        difference = 1 - total
        rhs = [['%s' % key, '%f' % (float(val) / tot_count)]
                for key, val in self.expansion.iteritems()
                if key]
        shuffle(rhs)
        delta = int(round(difference / 0.000001))
        for idx in range(abs(delta)):
            if delta > 0:
                rhs[idx][1] = '%f' % (float(rhs[idx][1]) + 0.000001)
            elif delta < 0:
                rhs[idx][1] = '%f' % (float(rhs[idx][1]) - 0.000001)
        rhs = ['%s [%s]' % (key, val) for key, val in rhs]
        regex = r'.*\[([01]\.\d+)\].*'
        check_total = 0
        for element in rhs:
            m = match(regex, element)
            check_total += float(m.group(1))

        return template % (self.variable, ' | '.join(rhs))


def parse(tree):
    lhs = tree.node.rstrip('$')
    if lhs not in tags:
        return
    rhs = []
    for subtree in tree:
        if isinstance(subtree, Tree) and subtree.node in tags:
            rhs.append(subtree.node.rstrip('$'))
        elif isinstance(subtree, basestring):
            if len(subtree.replace('\'', '')):
                rhs.append("'%s'" % subtree.replace('\'', ''))

    production = productions.get(lhs, Production(lhs))
    production.add(' '.join(rhs))

    productions[lhs] = production
    
    for subtree in tree:
        if isinstance(subtree, Tree):
            parse(subtree)


if __name__ == '__main__':
    tag_counter = Counter()
    for tree in treebank.parsed_sents():
        tag_counter.update(Counter([subtree.node.rstrip('$') for subtree in
                                    tree.subtrees()]))
    tags = set([tag for tag in tag_counter.iterkeys() if tag_counter[tag] > 100])
    stop_tags = ['.', '', ',', '``', '\'\'', ':', '-LRB-', '-RRB-', '-NONE-']

    for tag in stop_tags:
        if tag in tags: tags.remove(tag)
    for tree in treebank.parsed_sents():
        parse(tree)
    with open('grammar.pcfg', 'w') as f:
        root = productions.pop('S')
        f.write('%s\n' % root.to_string())
        for production in productions.itervalues():
            f.write('%s\n' % (production.to_string()))

