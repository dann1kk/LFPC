def CheckLeftRecursion(P):
    for key in P:
        for value in P[key]:
            if value[0] == key:  # if C -> C c return key
                return True, key

    return False, ''


def CheckLeftFactoring(P):
    for key in P:
        for value in P[key]:
            if value.find(key) > 1:  # check for match, if true return key
                return True, key

    return False, ''


def CheckFirst(F, NT):
    for key in F:
        for value in F[key]:
            if value[0] in NT:  # check first rhs to be Nt
                return True

    return False
