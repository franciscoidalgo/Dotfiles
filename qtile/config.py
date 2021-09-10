# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401
from collections import namedtuple

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import os
import subprocess

from my_widgets import QuickShutdown

mod = "mod4"
terminal = "kitty"

def alt_mod():
    if mod == "mod4":
        return "mod1"
    else:
        return "mod4"


Color_set  = namedtuple('Color_set', 'normal focus')
my_colors= Color_set('#061d1b', '#009688')

keys = [
    # Multimedia
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pavolume volup --quiet")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pavolume voldown --quiet")),
    Key([], "XF86AudioMute", lazy.spawn("pavolume mutetoggle --quiet")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set 10%+")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    # Custom ones babe
    Key([alt_mod()], "Tab", lazy.spawn('rofi -show window'), desc="Launches rofi window manager"),
    Key([mod], "e", lazy.spawn('rofi -show drun'), desc="Launches rofi program list"),
    Key([mod], "f", lazy.spawn('rofi -show filebrowser'), desc="Launches rofi file browser"),
    Key([mod], "s", lazy.spawn(terminal + ' fish'), desc="Launches fish shell"),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

groups = [
    Group(name, **kwargs)
    for name, kwargs in [
            ("WEB", {"matches": [Match(wm_class=["firefox"])]}),
            ("DEV1", {}),
            ("DEV2", {}),
            ("MISC", {}),
            ("DISC", {"matches": [Match(wm_class=["discord"])]}),
            ("MUS", {"matches": [Match(wm_class=["spotify"])]}),
            ("FM", {"matches": [Match(wm_class=["thunar"])]}),
            ("DOOM",{"matches": [Match(wm_class=["emacs"])], "persist":False, "init":False, "layout":'max'})
    ]
]

for i, group in enumerate(groups, 0):
    keys.extend(
        [
            Key(
                [mod], str(i), 
                lazy.group[group.name].toscreen(toggle=False),
                desc="Switch to group {group.name}"
            ),
            Key(
                [mod, "shift"], str(i),
                lazy.window.togroup(group.name),
                desc="Move focused window to group {group.name}"
            )
        ]
    )

layouts = [
    # layout.Bsp(
    #    border_focus=my_colors.focus,
    #    border_focus_stack='#479e8e', 
    #    border_normal='#1b413a', 
    #    border_normal_stack='#1b413a'),
    # layout.MonadTall(
    #    border_focus=my_colors.focus,  
    #    border_normal=my_colors.normal
    # ),
    layout.Columns(
        border_focus=my_colors.focus,
        border_focus_stack=my_colors.focus,
        border_normal=my_colors.normal,
        border_normal_stack=my_colors.normal,
        margin= 1
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Matrix(), 
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Fira Code',
    fontsize=12,
    padding=4,
)
extension_defaults = widget_defaults.copy()

# Custom widget functions

def spam_disc():
    qtile.cmd_spawncmd("discord")

# Mouse Callbacks

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(width=65),
                widget.GroupBox(
                    this_current_screen_border=my_colors.focus,
                    borderwidth=2
                ),
                widget.Prompt(),
                widget.WindowName(),
                widget.Clock(format='%Y-%m-%d  %a  %I:%M %p'),
                widget.PulseVolume(fmt='Vol {}'),
                widget.Systray(),
                widget.Battery(
                    format='{percent:2.0%}',
                    notify_below=30
                ),
                widget.BatteryIcon(theme_path='/usr/share/icons/Paper'),
                widget.Sep(linewidth=3, padding = 0, size_percent= 100, foreground=my_colors.normal),
                widget.QuickExit(
                    background=my_colors.focus,
                    default_text='Logout ︁',
                    countdown_format='   {}   ︁'
                ),
                widget.Sep(linewidth=2, padding = 0, size_percent= 100, foreground=my_colors.normal),
                widget.Sep(linewidth=2, padding = 0, size_percent= 100, foreground=my_colors.focus),
                QuickShutdown(
                    background=my_colors.normal
                )
            ],
            24,
        ),
        top=bar.Bar(
            [
                widget.Spacer(length = bar.STRETCH),
                widget.Wlan(interface='wlp6s0'),
                widget.CPU(),
                widget.Memory()
            ],
            size=10,
            #opacity=0.5
            background="#111111"
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# Startup function
@hook.subscribe.startup_once
def autostart():
    process_path = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([process_path])
    lazy.group["DEV1"].toscreen(toggle=False)

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
