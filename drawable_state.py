from state import State

class DrawableState(State):
    def __init__(self, isInit = False, isFinish = False, x = 0, y = 0):
        State.__init__(self, isInit, isFinish)
        self._x = x
        self._y = y
        self._active = False
        
    def draw(self):
        if self._active:
            fill(0,255,0)
        elif not self._isInit:
            fill(255)
        else:
            fill(50,170, 200)
        stroke(0)
        strokeWeight(2)
        ellipseMode(CENTER)
        ellipse(self._x, self._y, 50, 50)
        if self._isFinish:
            stroke(125, 0, 125)
            ellipse(self._x, self._y, 40, 40)
            
    def handleClick(self, cX, cY):
        return dist(self._x, self._y, cX, cY) <= 50
    
    def moveTo(self, x, y):
        self._x = x
        self._y = y
        
    def getX(self):
        return self._x
    
    def getY(self):
        return self._y
    
    def setActive(self,nval):
        self._active = nval
