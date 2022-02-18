from graphNFA import drawNFA
from graphDFA import drawDFA
from NFA import getNFA, transitions
from DFA import NFAtoDFA
import pandas as pd
import copy


print("NFA:")
nfa = getNFA(transitions)
dict1 = copy.deepcopy(nfa)
print(nfa)
for keys in dict1.copy():
    if keys.isdigit():
        dict1['q' + keys] = dict1[keys]
        del dict1[keys]

for val in dict1.values():
    for x, y in val.items():
        if len(y) == 2:
            new_x = 'q' + y[0] + 'q' + y[1]
            val[x] = new_x

        if len(y) == 1:
            new_x = 'q' + y
            val[x] = new_x

NFA = pd.DataFrame(dict1)
NFA = NFA.fillna("-")
drawNFA()
print(NFA.transpose())


print("\n DFA:")
dfa = NFAtoDFA(nfa)
print(dfa)
dict2 = copy.deepcopy(dfa)

for keys in dict2.copy():
    if keys.isdigit():
        if len(keys) == 2:
            dict2['q' + keys[0] + 'q' + keys[1]] = dict2[keys]
            del dict2[keys]
        if len(keys) == 1:
            dict2['q' + keys] = dict2[keys]
            del dict2[keys]

for val in dict2.values():
    for x, y in val.items():

        if len(y) == 2:
            new_x = 'q' + y[0] + 'q' + y[1]
            val[x] = new_x

        if len(y) == 1:
            new_x = 'q' + y
            val[x] = new_x

DFA = pd.DataFrame(dict2)
DFA = DFA.fillna("-")
drawDFA()
print(DFA.transpose())

