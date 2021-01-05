# Deterministic and Nondeterministic Finite Automata Visualization
This is a program meant to visualize the operation of [Finite Automata](https://en.wikipedia.org/wiki/Deterministic_finite_automaton) (both Deterministic and Nondeterministic) . It is written in python, using the Processing for Python Library for the visualization. The user can build an automaton and provide it with input to see the process by which it computes. By default, the user is building a [Nondeterministic Finite Automaton](https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton) (NFA) with [epsilon transitions](https://en.wikipedia.org/wiki/Epsilon_transition) because that encompasses the function of Deterministic Finite Automata as well. After creating an NFA, the user can generate the equivalent DFA using the [Powerset Construction Method](https://en.wikipedia.org/wiki/Powerset_construction).

## Using the program
To use the program you need a working version of Processing for Python. Open the sketch (open the automata_vis.pyde file with Processing) and click the run button. The following list is all the information you need to know:
 1. Circles on the screen represent states.
 2. The blue circle is the starting state.
 3. Any circle with an inner purple circle is an accepting state.
 4. To create a new state, double click anywhere on the screen.
 5. To delete a state, double click it -- you cannot delete the initial state.
 6. To move a state, click and drag with your mouse.
 7. To designate a state as accepting, right click it.
 8. Curves connecting states represent transitions.
 9. The characters listed close to the curve are the characters such that if one of them is given to the source state, it transitions to the destination.
 10. For any curve, if it is concave up, the source is the left vertex; if it is concave down, it is the right vertex. 
 11. All states must define transitions for all characters of the alphabet (the default is [0,1])
 12. To create a transition, left click on any state.
 13. That will highlight it as selected (shown as a square around that state).
 14. Then click on another state.
 15. You will be prompted to provide a character for the transition, do that (by typing the character and hitting Enter), and it will appear on the screen.
 16. To remove a transition, repeat the same process you followed to create it.
 17. Typing will add to the input string, appearing on the top of the screen.
 18. Pressing Enter will give that string to the automaton.
 19. The active states of the automaton are highlighted in green.
 20. Typing toDFA in the input string will prompt the program to create an equivalent DFA from the NFA that is on the screen.
 21. Typing clear in the input string will reset everything.
 22. Enjoy!

