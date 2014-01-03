from pymake import *

@ignore
def helper():
    print 'helping'

def all():
    """All the shit. """
    print 'all'
    build()

def clean():
    """Clean shit. """
    print 'cleaning'

def build(depends=clean):
    """Build shit. """
    print 'building'

def withargs(arg1, arg2, depends=clean):
    """Demo with args. """
    print 'withargs'
    print arg1
    print arg2
