import configparser
import sys
import os

import subprocess
from subprocess import check_output

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import GLib, Gio, Gtk


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class GladeApplication(object):
    glade_file = os.path.join(BASE_DIR, 'optimus_tools.glade')

    def __init__(self):
        try:
            self.gtk_builder = Gtk.Builder.new_from_file(self.glade_file)
        except GObject.GError:
            raise OsError("Error reading GUI file")


class AppMainWindow(GladeApplication):
    def __init__(self, application, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.application = application

        self.gtk_builder.connect_signals({
            'btn_do_not_sleep': (self.btn_do_not_sleep, ),
            'btn_start_intel_virtual_output': (self.btn_start_intel_virtual_output, ),
            'close': (self.close, )
        })

        main_menu_bar = self.gtk_builder.get_object('main_menu')
        self.main_window = self.gtk_builder.get_object("main_window")
        self.main_window.set_application(application)

        self.main_window.show()


    def btn_do_not_sleep(self, item):
        print('NOT SLEEP CLICKED')

    def btn_start_intel_virtual_output(self, item):
        print('Starting Intel Virtual Output')
        try:
            intel_pid = check_output(["pidof", "intel-virtual-output"])
            print ("Process Exists")
        except subprocess.CalledProcessError:
            print ("Process doesnt exists. Starting a new instance")
        #$subprocess.run(["intel-virtual-output"])

    def close(self, *args):
        self.main_window.destroy()

    def get_window(self):
        return self.main_window


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, application_id="org.joepreludian.bumblebee_tools",
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)

        self.add_main_option("start-intel", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Start a service", None)

        self.add_main_option("start-display-inhibit", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Start a service", None)

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        self.main_window = AppMainWindow(self)  #Bootstrapping Window

    # Handle command line info
    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        if "start-intel" in options:
            print("Start Intel")

        elif "start-display-inhibit" in options:
            print ("Activate Inhibit")

        else:
            self.activate()

        return 0

    def on_about(self, action, param):
        about_dialog = AppAboutDialog(application=self, transient_for=self.main_window.get_window())

    def on_quit(self, action, param):
        self.quit()


def init():
    app = Application()
    app.run(sys.argv)
