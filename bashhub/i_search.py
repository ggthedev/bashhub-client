#!/usr/bin/env python

import npyscreen
import datetime
import curses

class CommandList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(CommandList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^I": self.when_add_record,
            "q":  self.exit_app,
            curses.ascii.ESC : self.exit_app
        })

    def exit_app(self, vl):
        self.parent.parentApp.switchForm(None)

    def display_value(self, vl):
        return "{0}".format(vl)

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EDITRECORDFM').value = act_on_this
        self.parent.parentApp.switchForm('EDITRECORDFM')


    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDITRECORDFM').value = None
        self.parent.parentApp.switchForm('EDITRECORDFM')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.myDatabase.delete_record(self.values[self.cursor_line][0])
        self.parent.update_list()


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

    def onStart(self):
        self.addForm("MAIN", CommandListDisplay)
        self.addForm("EDITRECORDFM", EditRecord)

if __name__ == '__main__':
    my_app = InteractiveSearch(["Some command", "and another one"])
    my_app.run()
