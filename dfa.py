from state import State

class DFA:
    def __init__(self, alphabet = ['0','1']):
        self._alphabet = alphabet
        self._states = [State(True, False)]
        self._transitions = {}

    def __len__(self):
        return len(self._states)

    def analyze(self, message):
        if not self._isValid():
            print('This DFA is missing some transitions')
            return False
        if not self._validMessage(message):
            print('The message has to consist of characters from the alphabet')
            return False

        return self._analyzeHelper(message, self._states[0])

    def _analyzeHelper(self, msg, curr):
        if len(msg) == 0:
            return curr.isFinal()
        return self._analyzeHelper(msg[1:],self._transitions[(curr, msg[0])])

    def getState(self, idx):
        return self._states[idx]

    def addState(self, state = State()):
        self._states.append(state)

    def removeState(self, state):
        if state.isInit():
            print('Cannot remove the initial state')
            return

        self._states.remove(state)
        for c in self._alphabet:
            self._transitions.pop((state, c),None)
        self._transitions = {k : self._transitions[k] for k in self._transitions if self._transitions[k] != state}

    def setTransition(self, src, wth, dst):
        self._transitions[(src,wth)] = dst

    def _validMessage(self, msg):
        res = True
        for c in msg:
            res = res and (c in self._alphabet)
        return res

    def _isValid(self):
        return len(self._transitions) == (len(self._alphabet) * len(self._states))

    def trim(self):
        visited = set()
        q = [self._states[0]]
        while len(q) > 0:
            front = q.pop(0)
            visited.add(front)
            for c in self._alphabet:
                if self._transitions[(front, c)] not in visited:
                    q.append(self._transitions[(front,c)])
        not_visited = [state for state in self._states if state not in visited]
        for unreachable in not_visited:
            self.removeState(unreachable)
