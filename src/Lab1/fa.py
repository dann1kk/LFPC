import networkx as nx
import matplotlib.pyplot as plt

# Variant 18
grammar = [
    'S->aA',
    'A->bS',
    'S->aB',
    'B->aC',
    'C->a',
    'C->bS'
]


def drawGraph():
    G = nx.DiGraph()
    G.add_edges_from(
        [('S', 'A'), ('A', 'S'), ('S', 'B'), ('B', 'C'),
         ('C', '$'), ('C', 'S')])

    val_map = {'S': 1.0,
               '$': 0.1}

    values = [val_map.get(node, 0.75) for node in G.nodes()]

    back_edge = [('A', 'S')]
    regular_edges = [edge for edge in G.edges() if edge not in back_edge]
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color=values, node_size=500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=dict([
        (('S', 'A'), 'a'),
        (('A', 'S'), 'b'),
        (('S', 'B'), 'a'),
        (('B', 'C'), 'a'),
        (('C', '$'), 'a'),
        (('C', 'S'), 'b')
    ])
                                 )
    nx.draw_networkx_edges(G, pos, edgelist=back_edge, arrows=True, connectionstyle="arc3,rad=0.3")
    nx.draw_networkx_edges(G, pos, edgelist=regular_edges, arrows=True)
    plt.show()


def parseGrammar(grammar):
    finiteAutomaton = {}
    # initiate the finiteAutomaton

    for grammarRules in grammar:
        rule = grammarRules.split('->')
        # new dictionary that has as key-0 value a list of non-terminal symbols and each of them will have it own
        #  dictionary where key-1 is the list of symbols( terminal/non-terminal from right-side)
        subGrammar = {
            0: list(rule[0])[0],
            1: list(rule[1])
        }  # now in the case if we don't have this non-terminal symbol in the initial dictionary we create a dictionary
        # in the automaton that has all relations of non-terminal symbol
        if not subGrammar[0] in finiteAutomaton:
            finiteAutomaton[subGrammar[0]] = {}

        if len(subGrammar[1]) == 1:
            subGrammar[1].append('$')
        # if on the right side is 1 the expression is final, and we assign $

        finiteAutomaton[subGrammar[0]][subGrammar[1][0]] = subGrammar[1][1]
        # in automaton dictionary first char is set as key that points to value that is the next char at right

    return finiteAutomaton


def testGrammar(fa, initial, final, inputWord):

    state = initial  # initial step that will show the coming steps

    currword = ""
    print(state + "->")

    for ch in inputWord:
        if state in fa and ch in fa[state]:
            # the state changes to value that key terminal points
            state = fa[state][ch]
            currword += ch
            generatedWord = currword + state
            print('->' + generatedWord)
        else:
            return False

    return state in final


drawGraph()
finiteAutomaton = parseGrammar(grammar)
print(finiteAutomaton)
while True:
    print('Test String: ')
    inputWord = input()
    if inputWord == '':
        break
    print(testGrammar(finiteAutomaton, 'S', {'$'}, inputWord))
