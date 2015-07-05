#!/usr/bin/env python

import npyscreen
import datetime
import curses
import time

class CommandList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(CommandList, self).__init__(*args, **keywords)
        self.command_handlers = {}

        # Any non highlited command handlers
        self.add_handlers({
            "q":  self.exit_app,
            curses.ascii.ESC : self.exit_app
        })

        # All handlers for when a command is highlighted
        self.add_command_handlers({
            curses.ascii.NL:  self.select_command,
            curses.ascii.CR:  self.select_command,
            curses.ascii.SP:  self.go_to_command_details,
            "i":  self.go_to_command_details
        })

    def exit_app(self, vl):
        self.parent.parentApp.switchForm(None)

    def display_value(self, vl):
        return "{0}".format(vl)

    def add_command_handlers(self, command_handlers):
        self.command_handlers = command_handlers
        # wire up to use npyscreens h_act_on_hightlited
        event_handlers = dict((key, self.h_act_on_highlighted) for (key, value) in
                command_handlers.items())
        self.add_handlers(event_handlers)

    def actionHighlighted(self, command, keypress):
        if keypress in self.command_handlers:
            return self.command_handlers[keypress](command)

    def go_to_command_details(self, command):
        self.parent.parentApp.getForm('EDITRECORDFM').value = command
        self.parent.parentApp.switchForm('EDITRECORDFM')

    def select_command(self, command):
        self.parent.parentApp.return_value = command
        self.parent.parentApp.switchForm(None)

class CommandListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = CommandList
    #COMMAND_WIDGET_CLASS = None

    def beforeEditing(self):
        self.wStatus1.value  = "Status Line "
        self.update_list()

    def update_list(self):
        self.wMain.values = self.parentApp.commands
        self.wMain.display()


class EditRecord(npyscreen.ActionForm):

    def __init__(self, *args, **keywords):
        super(EditRecord, self).__init__()
        self.add_handlers({
            "q":  self.previous_form,
            curses.ascii.ESC : self.exit_app
        })

    def create(self):
        self.value = None
        self.created   = self.add(npyscreen.TitleFixedText, name = "Created At:",)
        self.command   = self.add(npyscreen.TitleFixedText, name = "Command:",)

    def exit_app(self, vl):
        self.parentApp.switchForm(None)

    def previous_form(self, vl):
        self.parentApp.switchFormPrevious()

    def beforeEditing(self):
        if self.value:
            record = self.value
            self.name = "The Record"
            date_string = datetime.datetime.fromtimestamp(record.created/1000).strftime('%Y-%m-%d%H:%M:%S')
            self.created.value = date_string
            self.command.value = record.command
        else:
            self.command = "not found"

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()




class InteractiveSearch(npyscreen.NPSAppManaged):

    def __init__(self, commands, rest_client=None):
        super(InteractiveSearch, self).__init__()
        self.commands = commands
        self.rest_client = rest_client
        self.return_value = "that"

    def onStart(self):
        self.addForm("MAIN", CommandListDisplay)
        self.addForm("EDITRECORDFM", EditRecord)

