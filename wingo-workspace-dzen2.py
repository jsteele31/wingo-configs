#!/usr/bin/env python2
 
# This script is designed to have its output sent to a dock like dzen or xmobar.
#
# This script is cut ridiculously short by my xpybutil library. It allows us to 
# omit a lot of the nasty details of fetching properties windows.
#
# This script will only work with Openbox Multihead or Wingo
# (or any other WM that adopts my _NET_VISIBLE_DESKTOPS property).
 
markup = {
    'current':      '^fg(#FF9800)%s^fg()',
    'visible':      '^fg(#fecf35)%s^fg()',
    'hidden':       '^fg(#fecf35)%s^fg()',
    'hidden_empty': '^fg(#b8b8b8)%s^fg()',

}
 
import sys
import time
 
import xcb, xcb.xproto, xcb.xinerama
 
from xpybutil import conn as c, root
import xpybutil.event as event
import xpybutil.ewmh as ewmh
import xpybutil.util as util
import xpybutil.xinerama as xinerama
 
c.core.ChangeWindowAttributes(root, xcb.xproto.CW.EventMask,
                              [xcb.xproto.EventMask.PropertyChange])
c.flush()
 
sleep = False
visibles = None
while visibles is None:
    if sleep:
        time.sleep(1)
 
    currentdesk = ewmh.get_current_desktop().reply()
    visibles = ewmh.get_visible_desktops().reply()
    names = ewmh.get_desktop_names().reply()
    deskcnt = ewmh.get_number_of_desktops().reply()
    sleep = True
 
def do_output(visibles, currentdesk, names, deskcnt):
    out_visible = []
    out_hidden = []
 
    for visible in visibles:
        if visible == currentdesk:
            out_visible.append(markup['current'] % names[visible])
        else:
            out_visible.append(markup['visible'] % names[visible])
 
    clients = ewmh.get_client_list().reply()
    nonemptydesks = set()
    for client in clients:
        nonemptydesks.add(ewmh.get_wm_desktop(client).reply())
 
    for d in xrange(deskcnt):
        if d not in visibles:
            if d in nonemptydesks:
                out_hidden.append(markup['hidden'] % names[d])
            else:
                out_hidden.append(markup['hidden_empty'] % names[d])
 
    print '[%s] %s' % (' '.join(out_visible), ' '.join(out_hidden))
 
    sys.stdout.flush()
 
do_output(visibles, currentdesk, names, deskcnt)
 
when_output = set(['_NET_CURRENT_DESKTOP', '_NET_VISIBLE_DESKTOPS',
                  '_NET_DESKTOP_NAMES', '_NET_NUMBER_DESKTOPS'])
 
try:
    while True:
        event.read(block=True)
        for e in event.queue():
            if not isinstance(e, xcb.xproto.PropertyNotifyEvent):
                continue
 
            aname = util.get_atom_name(e.atom)
            if aname == '_NET_CURRENT_DESKTOP':
                currentdesk = ewmh.get_current_desktop().reply()
            elif aname == '_NET_VISIBLE_DESKTOPS':
                visibles = ewmh.get_visible_desktops().reply()
            elif aname == '_NET_DESKTOP_NAMES':
                names = ewmh.get_desktop_names().reply()
            elif aname == '_NET_NUMBER_OF_DESKTOPS':
                deskcnt = ewmh.get_number_of_desktops().reply()
 
            if aname in when_output:
                do_output(visibles, currentdesk, names, deskcnt)
 
        c.flush()
except IOError, xcb.Exception:
    print >> sys.stderr, "X connection lost!"