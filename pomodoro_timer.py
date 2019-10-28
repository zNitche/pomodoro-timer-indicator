import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk
from gi.repository import AppIndicator3
from gi.repository import GObject
from threading import Thread
import time


class PomodoroIndicator:
    def __init__(self):
        self.app = "pomodoro_indicator"
        iconpath = ""
        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath, AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label("Pomodoro", self.app)

        self.dead = True
        self.brdead = True
        self.minutes = 25
        self.secs = 0
        self.brminutes = 30
        self.times = 1
        self.rounds = 4

    def create_menu(self):
        menu = Gtk.Menu()
        name = Gtk.MenuItem("Pomodoro")
        name.set_sensitive(False)
        menu.append(name)
        sep = Gtk.SeparatorMenuItem()
        menu.append(sep)
        start = Gtk.MenuItem('Start')
        start.connect('activate', self.start)
        menu.append(start)
        reset = Gtk.MenuItem('Reset')
        reset.connect('activate', self.reset)
        menu.append(reset)
        sep1 = Gtk.SeparatorMenuItem()
        menu.append(sep1)
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def start(self, source):
        if self.dead == True and self.brdead == True:
            self.update = Thread(target=self.time)
            self.update.setDaemon(True)
            self.update.start()
        else:
            pass

    def reset(self, source):
        if self.dead == False or self.brdead == False:
                self.dead = True
                self.brdead = True
                self.minutes = 25
                self.secs = 0
                self.times = 1
                self.rounds = 4
                self.brminutes = 30
                data1 = "Pomodoro"
                GObject.idle_add(self.indicator.set_label, data1, self.app, priority=GObject.PRIORITY_DEFAULT)
        else:
            self.brdead = True
            self.dead = True

    def time(self):
        self.brdead = True
        self.dead = False

        while (self.dead == False):
            if self.brdead == True:
                if self.minutes < 10 and self.secs < 10:
                    data = (f"Round {self.times} of {self.rounds} : 0{self.minutes}-0{self.secs}")

                elif self.minutes < 10:
                    data = (f"Round {self.times} of {self.rounds} : 0{self.minutes}-{self.secs}")

                elif self.secs < 10:
                    data = (f"Round {self.times} of {self.rounds} : {self.minutes}-0{self.secs}")

                else:
                    data = (f"Round {self.times} of {self.rounds} : {self.minutes}-{self.secs}")

                if self.secs == 0:
                    self.minutes -= 1
                    self.secs = 60

                if self.minutes < 0:
                    self.times += 1
                    self.minutes = 24

                if self.times > self.rounds:
                    self.secs = 60
                    self.brminutes -= 1
                    self.brdead = False

            else:
                self.brdead = False

                if self.brminutes < 10 and self.secs < 10:
                    data = (f"Break : 0{self.brminutes}-0{self.secs}")

                elif self.brminutes < 10:
                    data = (f"Break : 0{self.brminutes}-{self.secs}")

                elif self.secs < 10:
                    data = (f"Break : {self.brminutes}-0{self.secs}")

                else:
                    data = (f"Break : {self.brminutes}-{self.secs}")

                if self.secs == 0:
                    self.brminutes -= 1
                    self.secs = 60

                if self.brminutes < 0:
                    self.brminutes = 30
                    self.minutes = 24
                    self.times = 1
                    self.brdead = True

            self.secs -= 1
            GObject.idle_add(self.indicator.set_label, data, self.app, priority=GObject.PRIORITY_DEFAULT)
            time.sleep(1)

    def quit(self, source):
        Gtk.main_quit()


if __name__ == "__main__":

    PomodoroIndicator()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()