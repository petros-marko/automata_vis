from state import State

class NFA:
    def __init__(self, alphabet = ['0','1']):
        self._alphabet = alphabet + ['']
        self._states = [State(True, False)]
        self._transitions = {(s, c) : [] for s in self._states for c in self._alphabet}

    def __len__(self):
        return len(self._states)

    def analyze(self, message):
        if not self._isValid():
            print('This NFA is missing some transitions')
            return False
        if not self._validMessage(message):
            print('The message has to consist of characters from the alphabet')
            return False

        curr = [(self._states[0], message)]
        while len(curr) != 0:
            s, m = curr.pop(0)
            if len(m) == 0 and s.isFinal():
                return True
            curr.extend(map(lambda x: (x, m), self._transitions[(s, '')]))
            if len(m) > 0:
                curr.extend(map(lambda x: (x, m[1:]), self._transitions[(s, m[0])]))
        return False

    def getState(self, idx):
        return self._states[idx]

    def addState(self, state):
        self._states.append(state)
        for c in self._alphabet:
            self._transitions[(state, c)] = []

    def removeState(self, state):
        if state.isInit():
            print('Cannot remove the initial state')
            return

        self._states.remove(state)
        for c in self._alphabet:
            self._transitions.pop((state, c))
        for k in self._transitions:
            if state in self._transitions[k]:
                self._transitions[k].remove(state)

    def setTransition(self, src, wth, dst):
        self._transitions[(src,wth)].append(dst)

    def _validMessage(self, msg):
        res = True
        for c in msg:
            res = res and (c in self._alphabet)
        return res

    def _isValid(self):
        res = True
        for state in self._states:
            for c in self._alphabet:
                res = res and (c == '' or (len(self._transitions[(state,c)]) > 0))
        return res
