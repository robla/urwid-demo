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


class ExitPasterDemo():
    def __init__(self, exit_token=None):
        self.exit_token = exit_token


def get_buttons():
    """ renders the ok and cancel buttons."""

    # this is going to be what we actually do when someone clicks the button
    def ok_button_callback(button):
        raise ExitPasterDemo(exit_token='ok')
    okbutton = urwid.Button('OK', on_press=ok_button_callback)

    # second verse, same as the first....
    def cancel_button_callback(button):
        raise ExitPasterDemo(exit_token='cancel')
    cancelbutton = urwid.Button('Cancel', on_press=cancel_button_callback)

    return urwid.Columns([okbutton, cancelbutton])


def main():
    #  Our main loop is going to need a couple of things: 
    #  1. topmost widget - a "box widget" at the top of the widget hierarchy
    #  2. palette - style information for the UI
    
    #  1. topmost widget - a "box widget" at the top of the widget hierarchy
    fieldset = [
              ('Project name', 'project', 'text'),
              ('Version', 'version', 'text'),
              ('Description (one liner)', 'shortdesc', 'text'),
              ('Long description (multiline reStructuredText)', 'longdesc', 'text'),
              ('Author', 'authorname', 'text'),
              ('Author email', 'authoremail', 'text'),
              ('URL to project page', 'projecturl', 'text'),
              ('License', 'license', 'text'),
              ('Zip safe?', 'zipsafe', 'checkbox')
        ]

    # build the list of field widgets
    fieldwidgets = []
    for (label, inputname, fieldtype) in fieldset:
        if fieldtype == 'text':
            field = urwid.Edit(label + ': ', '')
        elif fieldtype == 'checkbox':
            field = urwid.CheckBox(label)
        fieldwidgets.append(field)

    fieldwidgets.append(get_buttons())

    # SimpleListWalker provides simple linear navigation between the widgets
    listwalker = urwid.SimpleListWalker(fieldwidgets)

    # ListBox is a scrollable frame around a list of elements
    listbox = urwid.ListBox(listwalker)

    #  2. palette - style information for the UI
    #  ....we'll get to this

    # Pass the topmost box widget to the MainLoop to start the show
    try:
        urwid.MainLoop(listbox, None).run()
    except ExitPasterDemo as inst:
        for i in range(len(fieldset)):
            print fieldset[i][0] + ':',
            if fieldset[i][2] == 'text':
                print fieldwidgets[i].get_edit_text()
            elif fieldset[i][2] == 'checkbox':
                print fieldwidgets[i].get_state()
        print "Exit value: " + inst.exit_token

if '__main__'==__name__:
    main()

