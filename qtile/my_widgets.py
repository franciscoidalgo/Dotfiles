from libqtile import bar
from libqtile.widget import base

class QuickShutdown(base._TextBox):
    
    defaults = [
        ('default_text', 'Shutdown ︁', 'A text displayed as a button'),
        ('countdown_format', '   {}     ︁', 'This text is showed when counting down.'),
        ('timer_interval', 1, 'A countdown interval.'),
        ('countdown_start', 5, 'Time to accept the second pushing.'),
    ]

    def __init__(self, widget=bar.CALCULATED, **config):
        base._TextBox.__init__(self, '', widget, **config)
        self.add_defaults(QuickShutdown.defaults)

        self.is_counting = False
        self.text = self.default_text
        self.countdown = self.countdown_start
        self.__call_later_funcs = []

        self.add_callbacks({'Button1': self.cmd_trigger})

    def __reset(self):
        self.is_counting = False
        self.countdown = self.countdown_start
        self.text = self.default_text
        for f in self.__call_later_funcs:
            f.cancel()

    def update(self):
        if not self.is_counting:
            return

        self.countdown -= 1
        self.text = self.countdown_format.format(self.countdown)
        func = self.timeout_add(self.timer_interval, self.update)
        self.__call_later_funcs.append(func)
        self.draw()

        if self.countdown == 0:
            self.qtile.cmd_spawn('shutdown now')
            self.__reset()
            self.draw()

    def cmd_trigger(self):
        if not self.is_counting:
            self.is_counting = True
            self.update()
        else:
            self.__reset()
            self.draw()