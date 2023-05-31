import os
from talon import Module, app

def set_up():
    from .master import setup
    setup()

app.register('ready', set_up)

module = Module()
@module.action_class
class Actions:
    pass
