from nfa import NFA
from drawable_state import DrawableState
from drawable_dfa import DrawableDFA
from threading import Thread
from time import sleep

class DrawableNFA(NFA):
    def __init__(self, alphabet = ['0','1'], x = 60, y = 355):
        self._alphabet = alphabet + ['']
        self._states = [DrawableState(True, False, x, y)]
        self._transitions = {(s, c) : [] for s in self._states for c in self._alphabet}
        self._selected = None
        self._callback = None
        self._choosingChar = False
        self._chosenChar = ''

    def draw(self):
        for (src, wth) in self._transitions:
            for dst in self._transitions[(src,wth)]:
                self._drawArrow(src, wth, dst)
            
        for state in self._states:
            state.draw()
            if self._selected == state:
                stroke(0)
                fill(0,0,0,0)
                rectMode(CENTER)
                rect(state.getX(),state.getY(), 60, 60)
                
            src = state
            for dst in self._states:
                chars = [(c if c != '' else '\\e') for c in self._alphabet if (src, c) in self._transitions and dst in self._transitions[(src,c)]]
                txt = ', '.join(chars)
                pushMatrix()
                sx, sy, dx, dy = src.getX(), src.getY(), dst.getX(), dst.getY()
                translate((sx + dx) / 2, (sy + dy) / 2)
                nsx, nsy, ndx, ndy = (sx - dx) / 2, (sy - dy) / 2, (dx - sx) / 2, (dy - sy) / 2
                a = atan2(ndy - nsy,ndx - nsx)
                rotate(a)
                textSize(25)
                textAlign(CENTER)
                fill(0,0,0,255)
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
        pushMatrix()
        translate((sx + dx) / 2, (sy + dy) / 2)
        nsx, nsy, ndx, ndy = (sx - dx) / 2, (sy - dy) / 2, (dx - sx) / 2, (dy - sy) / 2
        a = atan2(ndy - nsy,ndx - nsx)
        rotate(a)
        stroke(0)
        arc(0,0, dist(sx, sy, dx, dy), 2 * dist(sx,sy,dx,dy) / 3, 0, PI)
        popMatrix()
        
    def analyze(self, message):
        t = Thread(target = self._analyze, args = (message,))
        t.start()
        
    def _analyze(self, message):
        if not self._isValid():
            print('This NFA is missing some transitions')
            return False
        if not self._validMessage(message):
            print('The message has to consist of characters from the alphabet')
            return False

        curr = [(self._states[0], message)]
        while len(curr) != 0:
            for state, _ in curr:
                state.setActive(True)
            sleep(.4)
            for state, _ in curr:
                state.setActive(False)
            tmp = []
            while len(curr) > 0:
                s, m = curr.pop(0)
                if len(m) == 0 and s.isFinal():
                    return True
                tmp.extend(map(lambda x: (x, m), self._transitions[(s, '')]))
                if len(m) > 0:
                    tmp.extend(map(lambda x: (x, m[1:]), self._transitions[(s, m[0])]))
            curr = tmp
        return False
        
    def handleLeftClick(self):
        for state in self._states:
            if state.handleClick(mouseX, mouseY):
                if self._selected == None:
                    self._selected = state
                    return state
                else:
                    self._choosingChar = True
                    self._callback = lambda c : self._transitions[(self._selected, c)].remove(state) if state in self._transitions[(self._selected, c)] else self.setTransition(self._selected, c, state)
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
                if self._selected == state:
                    self._selected = None
                    self._choosingChar = False
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
            self._chosenChar = ''
        elif keyCode == BACKSPACE:
            self._chosenChar = ''
        else:
            self._chosenChar = key
        return True
    
    def toDFA(self):
        powerset = []
        for i in range(1, (1 << len(self._states))):
            sset = set()
            for j in range(len(self._states)):
                if i & (1 << j) != 0:
                    sset.add(self._states[j])
            powerset.append(sset)
    
        powerset = list(map(self._eclosure, powerset))
        #print(len(powerset))
        #print(powerset)
    
        alph = self._alphabet
        alph.remove('')
        dfa = DrawableDFA(alph, 50, 100)
    
        for state in powerset[0]:
            if state.isFinal():
                dfa.getState(0).setFinish(True)
    
        for i in range(1, len(powerset)):
            dfa.addState(DrawableState(False, False, 100 + 100 * (i % 14), 100 + 100 * (i // 8)))
            for state in powerset[i]:
                if state.isFinal():
                    dfa.getState(i).setFinish(True)
                    break
    
        for i in range(len(powerset)):
            for c in alph:
                dstSet = set()
                #print('setting transition for : ' + str((dfa.getState(i), c)))
                for s in powerset[i]:
                    dstSet = dstSet.union(self._eclosure(set(self._transitions[(s,c)])))
                dfa.setTransition(dfa.getState(i), c, dfa.getState(powerset.index(dstSet))) 
    
        dfa.trim()
        return dfa
