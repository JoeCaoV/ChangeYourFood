#!/usr/bin/env python3
# coding: utf-8

"""Main file that will start and run the GUI, it simply loads the
Display class then start the Display.home method
"""
from classes.display import Display

class Main:
    """I create a DOCSTRING here to please Pylint but to be honest,
    there is nothing very relevant to say, so instead I'm just wishing
    you a very good day to whoever reads this, glad you're here !
    """
    def __init__(self):
        """let's create our class and display home page"""
        display = Display()
        display.home()

if __name__ == "__main__":
    main = Main()
