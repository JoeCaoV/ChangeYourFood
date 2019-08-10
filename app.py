#!/usr/bin/env python3
# coding: utf-8

from classes.display import Display

class Main:

    def __init__(self):
        """let's create our class and display home page"""
        display = Display()
        display.home()

if __name__ == "__main__":
    main = Main()
