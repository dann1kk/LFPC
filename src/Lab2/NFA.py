transitions = [
    '0-a-0',
    '0-a-1',
    '1-b-2',
    '2-a-2',
    '3-a-3',
    '2-b-3'
]


def getNFA(transitions):
    nfa = {}
    for tr in transitions:
        x = tr.split('-')

        if not x[0] in nfa:
            nfa[x[0]] = {}

        if not x[1] in nfa[x[0]]:
            nfa[x[0]][x[1]] = ''

        nfa[x[0]][x[1]] += x[2]
    return nfa
