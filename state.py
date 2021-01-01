class State:
    def __init__(self, isInit = False, isFinish = False):
        self._isInit = isInit
        self._isFinish = isFinish

    def setInit(self, nval):
        self._isInit = nval
        
    def isInit(self):
        return self._isInit

    def setFinish(self, nval):
        self._isFinish = nval

    def isFinal(self):
        return self._isFinish
