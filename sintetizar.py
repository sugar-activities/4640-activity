#!/usr/bin/python

from subprocess import Popen


def sintetizar(text):
    Popen(['espeak', '-v', 'es', text])

