from os.path import join
from os import listdir, getcwd
import random

#@ignore
#def helper():
#    print 'helping'
#
def clean():
    """Clean shit. """
    sh('rm -rf test2')
    print 'Cleaned.'

def buildtwo():
    """Clean once, build twice."""
    build()
    build()
#
#directory("test2")
#file("test2/foo", "touch {}", depends="test2")
#
@depends(clean, clean)
def build():
    """Build shit. """
    ls = listdir(getcwd())
    n = len(ls)
    path = join(getcwd(), ls[random.randint(0, n-1)])
    sh("echo Building '{random}'")
    print 'building', getcwd()
#
#
@depends(
    build, 
    buildtwo,
#    "test2/foo"
)
def all():
    """All the shit. """
    print 'Complete.'
#    #build()
#    #buildtwo()
#
##all.depends = [build, buildtwo]
#
##all = build

def withargs(foo=0, bar=None):
    """Demo with args. """
    print 'withargs'
    print repr(foo)
