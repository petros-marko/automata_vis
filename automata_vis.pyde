from drawable_nfa import DrawableNFA
from drawable_dfa import DrawableDFA

dnfa = DrawableNFA()
inputString = ''

def setup():
    size(1440,760)
    print('Visualizing (Non)Deterministic Finite Automata:')
    print('Circles on your screen represent states')
    print('The blue circle is the starting state')
    print('Any circle with an inner purple circle is an accepting state')
    print('To create a new state, double click anywhere on the screen')
    print('To delete a state, double click it -- you cannot delete the initial state')
    print('To move a state, click and drag with your mouse')
    print('To designate a state as accepting, right click it')
    print('Curves connecting states represent transitions')
    print('The characters listed close to the curve are the characters such that if one of them is given to the source state, it transitions to the destination')
    print('For any curve, if it is concave up, the source is the left vertex; if it is concave down, it is the right vertex')
    print('All states must define transitions for all characters of the alphabet (default is [0,1])')
    print('To create a transition, left click on any state')
    print('That will highlight it as selected.')
    print('Then click on another state')
    print('You will be prompted to provide a character for the transition, do that, and it will appear on the screen')
    print('To remove a transition, repeat the same process you followed to create it')
    print('Typing will add to the input string, appearing on the top of the screen')
    print('Pressing return will give that string to the automaton')
    print('The active states of the automaton are highlighted in green')
    print('Typing toDFA in the input string will prompt the program to create an equivalent DFA from the NFA that is on the screen')
    print('Typing clear in the input string will reset everything')
    print('Enjoy')
    
def draw():
    background(255)
    dnfa.draw()
    fill(0)
    textSize(30)
    textAlign(LEFT)
    text('Input String: ' + inputString, 0, 30)
    
def mouseDragged(evt):
    dnfa.handleDrag()
    
def mouseClicked(evt):
    if evt.getCount() == 2:
        dnfa.handleDoubleClick()
    else:
        if mouseButton == LEFT:
            dnfa.handleLeftClick()
        else:
            dnfa.handleRightClick()
            
def keyTyped():
    global inputString
    global dnfa
    if not dnfa.handleKeyPresses():
        if key == '\n':
            if inputString == 'toDFA':
                inputString = ''
                dnfa = dnfa.toDFA()
            elif inputString == 'clear':
                inputString = ''
                dnfa = DrawableNFA()
            else:
                dnfa.analyze(inputString)
        elif key == BACKSPACE:
            inputString = '' if len(inputString) == 0 else inputString[:-1]
        else:
            inputString += key
