# This software may be used and distributed according to the terms
# of the GNU General Public License v2, incorporated herein by reference.
import sys

class ui:
    def __init__(self, verbose=False):
        self.verbose = verbose
    def note(self, str):
        if self.verbose:
            sys.stderr.write(str)
    def warn(self, str):
        sys.stderr.write(str)
        

