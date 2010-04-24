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

class ExitPasterDemo():
    def __init__(self, exit_token=None):
        self.exit_token = exit_token

class FieldManager(object):
    """ 
    This class manages the field data without being entangled in the 
    implementation details of the widget set.
    """
    def __init__(self):
        self.getters = {}

    def set_getter(self, name, function):
        """ 
        This is where we collect all of the field getter functions.
        """
        self.getters[name] = function
        
    def get_value(self, name):
        """
        This will actually get the value associated with a field name.
        """
        return self.getters[name]()

    def get_value_dict(self):
        """
        Dump everything we've got.
        """
        retval = {}
        for key in self.getters:
            retval[key] = self.getters[key]()
        return retval


def get_field(labeltext, inputname, fieldtype, fieldmgr):
    """ Build a field in our form.  Called from get_body()"""
    # we don't have hanging indent, but we can stick a bullet out into the 
    # left column.
    asterisk = urwid.Text(('label', '* '))
    label = urwid.Text(('label', labeltext))
    colon = urwid.Text(('label', ': '))

    if fieldtype == 'text':
        field = urwid.Edit('', '')
        def getter():
            """ 
            Closure around urwid.Edit.get_edit_text(), which we'll
            use to scrape the value out when we're all done.
            """
            return field.get_edit_text()
        fieldmgr.set_getter(inputname, getter)
    elif fieldtype == 'checkbox':
        field = urwid.CheckBox('')
        def getter():
            """ 
            Closure around urwid.CheckBox.get_state(), which we'll
            use to scrape the value out when we're all done. 
            """
            return field.get_state()
        fieldmgr.set_getter(inputname, getter)
    else:
        raise Exception()


    field = urwid.AttrWrap(field, 'field', 'fieldfocus')

    # put everything together.  Each column is either 'fixed' for a fixed width,
    # or given a 'weight' to help determine the relative width of the column
    # such that it can fill the row.
    editwidget = urwid.Columns([('fixed', 2, asterisk),
                                ('weight', 1, label),
                                ('fixed', 2, colon),
                                ('weight', 2, field)])

    wrapper = urwid.AttrWrap(editwidget, None, {'label':'labelfocus'})
    return urwid.Padding(wrapper, ('fixed left', 3), ('fixed right', 3))

def get_buttons():
    """ renders the ok and cancel buttons.  Called from get_body() """

    # this is going to be what we actually do when someone clicks the button
    def ok_button_callback(button):
        raise ExitPasterDemo(exit_token='ok')

    # leading spaces to center it....seems like there should be a better way
    b = urwid.Button('  OK', on_press=ok_button_callback)
    okbutton = urwid.AttrWrap(b, 'button', 'buttonfocus')

    # second verse, same as the first....
    def cancel_button_callback(button):
        raise ExitPasterDemo(exit_token='cancel')

    b = urwid.Button('Cancel', on_press=cancel_button_callback)
    cancelbutton = urwid.AttrWrap(b, 'button', 'buttonfocus')

    return urwid.GridFlow([okbutton, cancelbutton], 10, 7, 1, 'center')

def get_header():
    """ the header of our form, called from main() """
    text_header = ("'paster create' Configuration"
        " - Use arrow keys to select a field to edit, select 'OK'"
        " when finished, or press ESC/select 'Cancel' to exit")
    header = urwid.Text(text_header)
    return urwid.AttrWrap(header, 'header')

def get_body(fieldmgr):
    """ the body of our form, called from main() """
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
    fieldwidgets = [urwid.Divider(bottom=2)]
    for (label, inputname, fieldtype) in fieldset:
        fieldwidgets.append(get_field(label, inputname, fieldtype, fieldmgr))
    
    fieldwidgets.append(urwid.Divider(bottom=1)) 

    fieldwidgets.append(get_buttons())

    # SimpleListWalker provides simple linear navigation between the widgets
    listwalker = urwid.SimpleListWalker(fieldwidgets)
    
    # ListBox is a scrollable frame around a list of elements
    listbox = urwid.ListBox(listwalker)
    return urwid.AttrWrap(listbox, 'body')


def main():
    # call our homebrewed object for managing our fields
    fieldmgr = FieldManager()

    #  Our main loop is going to need four things: 
    #  1. frame - the UI with all of its widgets
    #  2. palette - style information for the UI
    #  3. screen - the engine used to render everything
    #  4. unhandled_input function - to deal with top level keystrokes
    
    #  1. frame - the UI with all of its widgets
    header = get_header()
    body = get_body(fieldmgr)
    frame = urwid.Frame(body, header=header)

    #  2. palette - style information for the UI
    palette = [
        ('body','black','white', 'standout'),
        ('header','black','light gray', 'bold'),
        ('labelfocus','black', 'white', 'bold, underline'),
        ('label','dark blue', 'white'),
        ('fieldfocus','black,underline', 'white', 'bold, underline'),
        ('field','black', 'white'),
        ('button','black','white'),
        ('buttonfocus','black','light gray','bold'),
        ]

    #  3. screen - the engine used to render everything
    screen = urwid.raw_display.Screen()

    #  4. unhandled_input function - to deal with top level keystrokes
    def unhandled(key):
        """ 
        Function to pass in to MainLoop to handle otherwise unhandled 
        keystrokes.
        """
        if key == 'esc':
            raise ExitPasterDemo(exit_token='cancel')

    # Putting it all together and running it
    try:
        urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled).run()
    except ExitPasterDemo as inst:
        import pprint
        pprint.pprint(fieldmgr.get_value_dict())
        print "Exit value: " + inst.exit_token

if '__main__'==__name__:
    main()

