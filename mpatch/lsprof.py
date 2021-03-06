# this is copied from the lsprof distro because somehow
# it is not installed by distutils
#
# small modifications made

import sys
try:
    from _lsprof import Profiler, profiler_entry, profiler_subentry
except ImportError, inst:
    import packagescan
    if packagescan.scan_in_progress:
        raise packagescan.SkipPackage('_lsprof not available')
    raise

__all__ = ['profile', 'Stats']

def profile(f, *args, **kwds):
    """XXX docstring"""
    p = Profiler()
    p.enable(subcalls=True)
    try:
        ret = f(*args, **kwds)
    finally:
        p.disable()
    return ret, Stats(p.getstats())


class Stats(object):
    """XXX docstring"""

    def __init__(self, data):
        self.data = data

    def sort(self, crit="inlinetime"):
        """XXX docstring"""
        if crit not in profiler_entry.__dict__:
            raise ValueError, "Can't sort by %s" % crit
        self.data.sort(lambda b, a: cmp(getattr(a, crit),
                                        getattr(b, crit)))
        for e in self.data:
            if e.calls:
                e.calls.sort(lambda b, a: cmp(getattr(a, crit),
                                              getattr(b, crit)))

    def pprint(self, top=None, file=None, limit=None, climit=None):
        """XXX docstring"""
        if file is None:
            file = sys.stdout
        d = self.data
        if top is not None:
            d = d[:top]
        cols = "% 12s %11.4f %11.4f   %s\n"
        hcols = "% 12s %12s %12s %s\n"
        cols2 = "+%12s %11.4f %11.4f +  %s\n"
        file.write(hcols % ("CallCount", "Total(s)",
                            "Inline(s)", "module:lineno(function)"))
        count = 0
        for e in d:
            file.write(cols % (e.callcount, e.totaltime,
                               e.inlinetime, label(e.code)))
            count += 1
            if limit is not None and count == limit:
                return
            ccount = 0
            if e.calls:
                for se in e.calls:
                    file.write(cols % ("+%s" % se.callcount,
                                       se.totaltime, se.inlinetime,
                                       "+%s" % label(se.code)))
                    count += 1
                    ccount += 1
                    if limit is not None and count == limit:
                        return
                    if climit is not None and ccount == climit:
                        break

    def freeze(self):
        """Replace all references to code objects with string
        descriptions; this makes it possible to pickle the instance."""

        # this code is probably rather ickier than it needs to be!
        for i in range(len(self.data)):
            e = self.data[i]
            if not isinstance(e.code, str):
                self.data[i] = type(e)((label(e.code),) + e[1:])
                if e.calls:
                    for j in range(len(e.calls)):
                        se = e.calls[j]
                        if not isinstance(se.code, str):
                            e.calls[j] = type(se)((label(se.code),) + se[1:])

_fn2mod = {}

def label(code):
    if isinstance(code, str):
        return code
    try:
        mname = _fn2mod[code.co_filename]
    except KeyError:
        sysmods = list(sys.modules.iteritems())
        for k, v in sysmods:
            if v is None:
                continue
            if not hasattr(v, '__file__'):
                continue
            if not isinstance(v.__file__, str):
                continue
            if v.__file__.startswith(code.co_filename):
                mname = _fn2mod[code.co_filename] = k
                break
        else:
            mname = _fn2mod[code.co_filename] = '<%s>'%code.co_filename

    return '%s:%d(%s)' % (mname, code.co_firstlineno, code.co_name)


if __name__ == '__main__':
    import os
    sys.argv = sys.argv[1:]
    if not sys.argv:
        print >> sys.stderr, "usage: lsprof.py <script> <arguments...>"
        sys.exit(2)
    sys.path.insert(0, os.path.abspath(os.path.dirname(sys.argv[0])))
    stats = profile(execfile, sys.argv[0], globals(), locals())
    stats.sort()
    stats.pprint()
