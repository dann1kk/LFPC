import string
from collections import Counter

import CheckGrammar


class LL1:

    def __init__(self, file):
        self.Follow = None
        self.column = None
        self.First = None
        with open(file) as f:
            input_lines = f.read().split('\n')

        self.non_terminal = list(input_lines[0].split())  # non terminals
        self.terminal = list(input_lines[1].split())  # terminal
        self.start = self.non_terminal[0]  # starting non-terminal
        self.letters = list(string.ascii_uppercase)  # available letters

        for char in self.non_terminal:
            self.letters.remove(char)
        self.P = {}
        self.new_value = False

        for line in input_lines[2:]:
            key, value = line.split()

            if key in self.P:
                self.P[key].append(value)
            else:
                self.P[key] = [value]

    def print(self):
        print('P={')
        for key in self.P:
            print(key, '-> ', end='')
            i = 0
            for value in self.P[key]:
                if i >= 1:
                    print('|', end='')  # add new product

                if value == '_':
                    print('ε', end='')  # add epsilon
                    i += 1
                else:
                    print(value + '', end='')
                    i += 1
            print()
        print('}')

    def Step1(self):
        LR, key = CheckGrammar.CheckLeftRecursion(self.P)
        if LR != 0:
            self.Left_Recursion_Elimination(key)
            self.print()
            self.Step1()
        else:
            return

    def Left_Recursion_Elimination(self, key):
        print('Eliminate Left Recursion for: ', key)
        alpha = []
        beta = []
        newLetter = self.letters[0]  # get next letter
        self.letters.remove(newLetter)  # remove it from unused letters
        self.non_terminal.append(newLetter)  # add it to non-terminal
        for value in self.P[key]:
            if value[0] == key:  # ex C -> C c
                alpha.append(value[1:] + newLetter)
            elif value == '_':
                beta.append(newLetter)
            else:
                beta.append(value + newLetter)  # C -> c E

        del self.P[key]
        self.P[key] = beta
        self.P[newLetter] = alpha
        self.P[newLetter].append('_')  # add epsilon

    def Step2(self):
        LF, key = CheckGrammar.CheckLeftFactoring(self.P)
        if LF != 0:
            self.Left_Factoring_Elimination(key)
            self.print()
            self.Step2()
        else:
            return

    def Left_Factoring_Elimination(self, key):
        print('Eliminating Left Factoring for:', key)
        T = []  # initialize a list with key products
        T.extend(self.P[key])
        min = 5
        for i in range(0, len(T)):  # check products length
            # if length is 1 add epsilon to it in new Nt
            if len(T[i]) < min:
                min = len(T[i])
            if T[i] == '_':
                T.remove('_')
        if len(T) == 1:
            i = 0
        else:
            for i in range(0, min):
                l = T[0][i]
                for value in T:
                    if (value[i] != l) or (value[i] == key):
                        break
            i += 1
        alpha = []
        beta = []
        letter = self.letters[0]  # add new non-terminal
        self.letters.remove(letter)
        self.non_terminal.append(letter)

        for value in self.P[key]:
            if value != '_':
                alpha.append(value[:i] + letter)
                beta.append(value[i:])
            else:
                alpha.append('_')

        if '' in beta:
            beta.remove('')
            beta.append('_')

        self.P[key] = list(set(alpha))
        self.P[letter] = list(set(beta))

    def Step3(self):
        # First terminals on rhs represent firsts

        self.First = {}  # create dictionar of firsts
        for key in self.non_terminal:
            self.First[key] = []
        for key in self.P:  # each key in grammar
            for value in self.P[key]:  # each value in keys
                if (value[0] in self.terminal):
                    self.First[key].append(value[0])  # if first value is terminal add it to first
                else:
                    self.First[key].append(value)
                self.First[key] = list(set(self.First[key]))
        while CheckGrammar.CheckFirst(self.First, self.non_terminal):
            for key in self.First:
                tab = []
                for value in self.First[key]:
                    if (value[0] in self.non_terminal) and ('_' in self.First[value[0]]) and (len(value) > 1):
                        tab.extend(self.First[value[0]])  # add epsilon
                        tab.remove('_')
                        tab.append(value[1:])

                    elif value[0] in self.non_terminal:
                        tab.extend(self.First[value[0]])

                    else:
                        tab.append(value)
                tab = list(set(tab))
                self.First[key] = tab

    def Step4(self):
        # Rules:
        # Put $ in start symbol S
        # B -> a A B , Follow A= First(B)
        self.Follow = {}
        for key in self.non_terminal:
            self.Follow[key] = []
        # Add $ to source
        self.Follow['S'].append('$')
        for key in self.P:
            for value in self.P[key]:
                for i in range(0, len(value)):
                    if value[i] in self.non_terminal:
                        if i == len(value) - 1:
                            self.Follow[value[i]].append(key)  # Add key to follow dict
                        elif value[i + 1] in self.terminal:
                            self.Follow[value[i]].append(value[i + 1])  # if terminal add value to dict
                        else:
                            tab = self.First[value[i + 1]]
                            if '_' in tab:
                                tab.remove('_')
                                tab.append(key)
                            self.Follow[value[i]].extend(tab)

        while CheckGrammar.CheckFirst(self.Follow, self.non_terminal):
            for key in self.Follow:  # for every key in follow set add missing values / or $
                tab = []
                for value in self.Follow[key]:
                    if (value in self.non_terminal) and (key not in self.Follow[value]):
                        tab.extend(self.Follow[value])
                    elif value in self.terminal or value == '$':
                        tab.append(value)
                tab = list(set(tab))
                self.Follow[key] = tab

    def ParsingTable(self):
        self.column = {}
        i = 0
        for key in self.terminal:
            self.column[key] = i
            i += 1
        self.column['$'] = i

        self.rows = {}
        for key in self.non_terminal:
            self.rows[key] = [''] * (len(self.terminal) + 1)

        for key in self.P:
            for value in self.P[key]: # add values in a and b
                a = []
                b = []
                if value[0] in self.terminal:
                    a.append(value[0])
                elif value[0] in self.non_terminal:
                    a.extend(self.First[value[0]])
                    if '_' in a:
                        a.remove('_')
                        b.extend(self.Follow[key])
                elif value == '_':
                    b.extend(self.Follow[key])

                for ter in b:
                    self.rows[key][self.column[ter]] = '_'
                for ter in a:
                    self.rows[key][self.column[ter]] = value
                    # print each row of table
                    print(f"{key} {self.rows[key]}")

    def ParseString(self, word):
        Stack = 'S$'
        Input = word + '$'
        Err = False
        print(' Stack |    Buffer    | Action ')
        while not Err:
            coll = ' ' * (7 - len(Stack))
            coll2 = ' ' * (13 - len(Input))
            print(Stack + coll + '|', Input + coll2 + '|', end=' ')
            Err, Stack, Input, Action = self.AcceptString(Stack, Input)
            print(Action)
        print()

        if Stack == '$' and Input == Stack:
            print('String Accepted!')
        else:
            print('String Not Accepted!')

    def AcceptString(self, Stack, Input):
        if Stack == '$':
            return True, Stack, Input, 'Done!'
        if Stack[0] == Input[0]:
            return False, Stack[1:], Input[1:], '-'
        new = self.rows[Stack[0]][self.column[Input[0]]]
        if new == '_':
            return False, Stack[1:], Input, 'ε'
        elif new != '_':
            return False, new + Stack[1:], Input, new
        else:
            return True, '', '', ''

    def Parse(self, word):
        print("Initial Grammar:")
        self.print()
        self.Step1()
        self.Step2()
        print('Firsts:')
        self.Step3()
        print(self.First)
        print('Follows:')
        self.Step4()
        print(self.Follow)
        print('Parsing Table:')
        x = '   '
        print(x, end=' ')
        print(*self.terminal, sep='   ', end=' ')
        print("  $")
        self.ParsingTable()

        self.ParseString(word)


L = LL1('grammar.txt')

L.Parse('abcdeabcccd')
