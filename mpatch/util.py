"""
util.py - Mercurial utility functions and platform specfic implementations

 Copyright 2005 K. Thananchayan <thananck@yahoo.com>
 Copyright 2005, 2006 Matt Mackall <mpm@selenic.com>
 Copyright 2006 Vadim Gelfer <vadim.gelfer@gmail.com>

This software may be used and distributed according to the terms
of the GNU General Public License, incorporated herein by reference.

This contains helper routines that are independent of the SCM core and hide
platform-specific details from the core.
"""

import os

class Abort(Exception): pass

def set_exec(f, mode):
    s = os.lstat(f).st_mode
    if (s & 0100 != 0) == mode:
        return
    if mode:
        # Turn on +x for every +r bit when making a file executable
        # and obey umask.
        umask = os.umask(0)
        os.umask(umask)
        os.chmod(f, s | (s & 0444) >> 2 & ~umask)
    else:
        os.chmod(f, s & 0666)
