from state import State

class DFA:
    def __init__(self, alphabet = ['0','1']):
        self._alphabet = alphabet
        self._states = [State(True, False)]
        self._transitions = {}

    def __len__(self):
        return len(self._states)

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
