def NFAtoDFA(nfa):
    states = []
    values = []

    # copy the states
    for state in nfa:
        states.append(state)

    # searching for new states
    for state in nfa:
        for value in nfa[state]:
            # if the length of a state is bigger than 1, we add the new state
            if len(nfa[state][value]) > 1:
                if not nfa[state][value] in states:
                    states.append(nfa[state][value])
            else:
                if not nfa[state][value][0] in states:
                    states.append(nfa[state][value][0])

    for state in nfa:
        for value in nfa[state]:
            if not value in values:
                values.append(value)

    for state in states:
        if state not in nfa:
            # spliting the states into an array, q0q1 = ['0','1']
            newState = list(state)
            for value in values:
                val = []

                # add the transitions of the new state
                for st in newState:
                    if value in nfa[st]:
                        val.append(nfa[st][value])
                # we add the new state in the global dict keyed by states
                if state not in nfa:
                    nfa[state] = {}
                # add the elements of the list to the inner dict which is keyed by alphabet elements
                # the values in the inner dict are joined as all the transitions from the formed state are considered
                nfa[state][value] = ''.join(set(''.join(val)))
                states.append(''.join(set(''.join(val))))
    return nfa
