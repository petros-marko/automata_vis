from dfa import DFA
from drawable_state import DrawableState
from time import sleep
from threading import Thread

class DrawableDFA(DFA):
    def __init__(self, alphabet = ['0','1'], x = 60, y = 355):
        DFA.__init__(self, alphabet)
        self._states[0] = DrawableState(True, False, x, y)
        self._selected = None
        self._callback = None
        self._choosingChar = False
        self._chosenChar = ''
        
    def draw(self):
        for (src, wth) in self._transitions:
            self._drawArrow(src, wth, self._transitions[(src,wth)])
            
        for state in self._states:
            state.draw()
            if self._selected == state:
                stroke(0)
                fill(0,0,0,0)
                rectMode(CENTER)
                rect(state.getX(),state.getY(), 60, 60)
                
            src = state
            for dst in self._states:
                chars = [c for c in self._alphabet if (src, c) in self._transitions and self._transitions[(src,c)] == dst]
                txt = ', '.join(chars)
                pushMatrix()
                sx, sy, dx, dy = src.getX(), src.getY(), dst.getX(), dst.getY()
                translate((sx + dx) / 2, (sy + dy) / 2)
                nsx, nsy, ndx, ndy = (sx - dx) / 2, (sy - dy) / 2, (dx - sx) / 2, (dy - sy) / 2
                a = atan2(ndy - nsy,ndx - nsx)
                rotate(a)
                textSize(25)
                fill(0,0,0,255)
                textAlign(CENTER)
                translate(0, dist(sx,sy,dx,dy) / 3 + 30)
                rotate(-a)
                text(txt, 0, 0)
                popMatrix()
                
        if self._choosingChar:
            fill(0)
            textSize(30)
            textAlign(CENTER)
            text('Choose a character of the transition and hit enter', width / 2, height / 3)       
                            
    def _drawArrow(self, src, wth, dst):
        sx, sy, dx, dy = src.getX(), src.getY(), dst.getX(), dst.getY()
        fill(0,0,0,0)
        updown = ord(wth) % 2 == 0
        pushMatrix()
        translate((sx + dx) / 2, (sy + dy) / 2)
        nsx, nsy, ndx, ndy = (sx - dx) / 2, (sy - dy) / 2, (dx - sx) / 2, (dy - sy) / 2
        a = atan2(ndy - nsy,ndx - nsx)
        rotate(a)
        stroke(0)
        arc(0,0, dist(sx, sy, dx, dy), 2 * dist(sx,sy,dx,dy) / 3, 0, PI)
        popMatrix()
        
    def _analyzeHelper(self, msg, curr):
        t = Thread(target = self._analyzeRec, args = (msg, curr))
        t.start()
    
    def _analyzeRec(self, msg, curr):
        curr.setActive(True)
        redraw()
        sleep(.4)
        curr.setActive(False)
        sleep(.1)
        if len(msg) == 0:
            return curr.isFinal()
        return self._analyzeRec(msg[1:],self._transitions[(curr, msg[0])])
        
    def handleLeftClick(self):
        for state in self._states:
            if state.handleClick(mouseX, mouseY):
                if self._selected == None:
                    self._selected = state
                    return state
                else:
                    self._choosingChar = True
                    self._chosenChar = ''
                    self._callback = lambda c : self._transitions.pop((self._selected, c), None) if (self._selected, c) in self._transitions and state == self._transitions[(self._selected, c)] else self.setTransition(self._selected, c, state)
                    return state
        self._selected = None
        
    def handleRightClick(self):
        for state in self._states:
            if state.handleClick(mouseX, mouseY):
                state.setFinish(not state.isFinal())
        
    def handleDoubleClick(self):
        for state in self._states:
            if state.handleClick(mouseX, mouseY):
                self.removeState(state)
                if self._selected == state or self._choosingChar:
                    self._selected = None
                return state
        self.addState(DrawableState(False, False, mouseX, mouseY))
        
    def handleDrag(self):
        for state in self._states:
            if state.handleClick(pmouseX, pmouseY):
                state.moveTo(mouseX, mouseY)
                return state
            
    def handleKeyPresses(self):
        if not self._choosingChar:
            return False
        if key == '\n':
            self._callback(self._chosenChar)
            self._choosingChar = False
            self._callback = None
            self._selected = None
        elif keyCode == BACKSPACE:
            self._chosenChar = ''
        else:
            self._chosenChar = key
        return True
        
