#!/usr/bin/python
# Paster create demo - this is an example of a possible user interface to the
#   "paster create" command out of Python Paste
# Copyright (c) 2010 Rob Lanphier
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import urwid
import urwid.raw_display


def get_field(labeltext, inputname):
    """ Build a field in our form.  Called from get_body()"""
    label = urwid.Text(labeltext)
    field = urwid.Edit('', '')
    # put the label and field together.
    return urwid.Columns([label, field])

def get_header():
    """ the header of our form, called from main() """
    text_header = ("'paster create' Configuration"
        " - Use arrow keys to select a field to edit, press ESC to exit")
    return urwid.Text(text_header)

def get_body():
    """ the body of our form, called from main() """
    fieldset = [
              ('Project name', 'project'),
              ('Version','version'),
              ('Description (one liner)','shortdesc'),
              ('Long description (multiline reStructuredText)', 'longdesc'),
              ('Author','authorname'),
              ('Author email','authoremail'),
              ('URL to project page','projecturl'),
              ('License','license'),
              ('Zip safe?','zipsafe')
        ]

    # build the list of field widgets
    fieldwidgets = [urwid.Divider(bottom=2)]
    for (label, inputname) in fieldset:
        fieldwidgets.append(get_field(label, inputname))
    
    # SimpleListWalker provides simple linear navigation between the widgets
    listwalker = urwid.SimpleListWalker(fieldwidgets)
    
    # ListBox is a scrollable frame around a list of elements
    return urwid.ListBox(listwalker)


def main():
    #  Our main loop is going to need four things: 
    #  1. frame - the UI with all of its widgets
    #  2. palette - style information for the UI
    #  3. screen - the engine used to render everything
    #  4. unhandled_input function - to deal with top level keystrokes
    
    #  1. frame - the UI with all of its widgets
    header = get_header()
    body = get_body()
    frame = urwid.Frame(body, header=header)

    #  2. palette - style information for the UI
    #  ....we'll get to this
    
    #  3. screen - the engine used to render everything
    screen = urwid.raw_display.Screen()

    #  4. unhandled_input function - to deal with top level keystrokes
    def unhandled(key):
        """ 
        Function to pass in to MainLoop to handle otherwise unhandled 
        keystrokes.
        """
        if key == 'esc':
            raise urwid.ExitMainLoop()

    # Putting it all together and running it
    urwid.MainLoop(frame, None, screen, unhandled_input=unhandled).run()

if '__main__'==__name__:
    main()

