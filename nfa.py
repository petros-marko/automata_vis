from state import State

class NFA:
    def __init__(self, alphabet = ['0','1']):
        self._alphabet = alphabet + ['']
        self._states = [State(True, False)]
        self._transitions = {(s, c) : [] for s in self._states for c in self._alphabet}

    def __len__(self):
        return len(self._states)

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
