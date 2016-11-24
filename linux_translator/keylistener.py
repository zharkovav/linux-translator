"""Keyaborad listener"""

import sys

import pyxhook

action_callback = None
exit_callback = None


def hook_exit():
    """Cancel hook and exit"""
    new_hook.cancel()
    sys.exit()


def onkeypress(event):
    """Key pressed Hook"""
    if event.Key == 'F9':
        if callable(exit_callback):
            exit_callback()
        hook_exit()
    elif event.Key == 'F2':
        if callable(action_callback):
            action_callback()


# instantiate HookManager class
new_hook = pyxhook.HookManager()

# listen to all keystrokes
new_hook.KeyDown = onkeypress

# hook the keyboard
new_hook.HookKeyboard()
