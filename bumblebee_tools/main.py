import os
import sys
import subprocess
import configparser

from time import sleep
from threading import Thread
from subprocess import check_output

from pynput.mouse import Button, Controller

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import GLib, Gio, Gtk, Notify
from gi.repository.Gio import File


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mouse_handler = Controller()
is_inhibit_on = False

def do_start_intel():
    print('Starting Intel Virtual Output')
    try:
        intel_pid = check_output(["pidof", "intel-virtual-output"])
        print ("Process Exists")
        hello = Notify.Notification.new("Bumblebee Tools", "Intel Virtual Output is already running.", "dialog-information")
        hello.show()


    except subprocess.CalledProcessError:
        print ("Process doesnt exists. Starting a new instance")
        subprocess.run(["intel-virtual-output"])

        hello = Notify.Notification.new("Bumblebee Tools", "Enabling Intel Virtual Output", "dialog-information")
        hello.show()


def do_toggle_inhibit():
    global is_inhibit_on
    global mouse_handler

    is_inhibit_on = not is_inhibit_on

    is_inhibit_on_str = 'ON' if is_inhibit_on else 'OFF'
    hello = Notify.Notification.new(
        "Bumblebee Tools", 
        f"Enable Inhibit {is_inhibit_on_str}", 
        "dialog-information")

    if is_inhibit_on:
        thread = Thread(target=do_inhibit_thread, 
                        args=(mouse_handler, lambda: not is_inhibit_on))
        thread.start()

    hello.show()

    return is_inhibit_on

def do_stop_inhibit():
    global is_inhibit_on
    is_inhibit_on = False
    print('Stop Inhibit')

def do_inhibit_thread(mouse_hander, stop_flag):
    while True:
        sleep(5)
        mouse_handler.move(10, -10)
        mouse_handler.move(-10, 10)

        print('Acting')
        if stop_flag():
            print('Break Thread detected. Stopping')
            break


class GladeApplication(object):
    glade_file = None

    def __init__(self):
        try:
            glade_file = os.path.join(BASE_DIR, self.glade_file)
            self.gtk_builder = Gtk.Builder.new_from_file(glade_file)
        except GObject.GError:
            raise OsError("Error reading GUI file")

    def get_window(self):
        return self.main_window



class AppAboutWindow(GladeApplication):

    glade_file = 'about_window.glade'

    def __init__(self, application, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.application = application

        self.gtk_builder.connect_signals({
            'btn_open_github': (self.btn_open_github, ),
            'close': (self.close, )
        })

        self.main_window = self.gtk_builder.get_object("about_window")
        self.main_window.set_application(application)
        self.main_window.show()

    def btn_open_github(self, item):
        Gtk.show_uri_on_window(self.main_window, 'https://github.com/joepreludian/bumblebee_tools', 1)

    def close(self, *args):
        print('Close about')
        self.main_window.destroy()



class AppMainWindow(GladeApplication):

    glade_file = 'main_window.glade'

    def __init__(self, application, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.application = application

        self.gtk_builder.connect_signals({
            'btn_open_about': (self.btn_open_about,), 
            'btn_do_not_sleep': (self.btn_do_not_sleep, ),
            'btn_start_intel_virtual_output': (self.btn_start_intel_virtual_output, ),
            'on_destroy': (self.close, )
        })

        self.main_window = self.gtk_builder.get_object("main_window")
        self.main_window.set_application(self.application)

        self.main_window.show()

    def btn_open_about(self, item):
        self.about_window = AppAboutWindow(self.application)

    def btn_do_not_sleep(self, item):
        do_toggle_inhibit()

    def btn_start_intel_virtual_output(self, item):
        do_start_intel()

    def close(self, *args):
        print('Closing main')
        do_stop_inhibit()
        self.main_window.destroy()


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, application_id="org.joepreludian.bumblebee_tools",
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)

        self.add_main_option("start-intel", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Start Intel Virtual Output", None)

        self.add_main_option("start-display-inhibit", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Start and enable display inhibit", None)

        self.register()
        Notify.init("Bumblebee Tools")

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        self.main_window = AppMainWindow(self)  #Bootstrapping Window

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()

        if "start-intel" in options:
            do_start_intel()
        elif "start-display-inhibit" in options:
            do_toggle_inhibit()
            self.activate()
        else:
            self.activate()

        return 0

    def on_quit(self, action, param):
        print ('Exitting')
        self.quit()


def init():
    app = Application()
    app.run(sys.argv)

if __name__ == '__main__':
    init()
