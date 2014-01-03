#!/usr/bin/env python
from collections import Iterable
from functools import wraps
import argparse
import inspect
import imp
import sys
import re
import os
# could simplify a lot of this by just puttnig a 
pymake = imp.new_module('pymake')
dummy = imp.new_module('dummy')

# TODO moving this into a separate file would give us syntax highlighting, 
# potentially linking w other modules, etc etc.
helpers = """
def ignore(func):
    func.ignored = True
    return func
"""

exec helpers in pymake.__dict__
exec helpers in dummy.__dict__

fname = "Pymake"
if not os.path.exists(fname):
    print 'No Pymake file found. Exiting...'

with open(fname) as f:
    code = f.read()
    exec code in pymake.__dict__

functions = sorted(dir(pymake))
for f in dir(dummy):
    functions.remove(f)

DEPEND = 'depends'

def add_function(subparsers, f):
    func = pymake.__getattribute__(f)
    if getattr(func, 'ignored', False) or not inspect.isfunction(func):
        return
    subparser = subparsers.add_parser(f, help=func.__doc__, description=func.__doc__)
    args, varargs, keywords, defaults = inspect.getargspec(func)
    if defaults:
        defaults = dict(zip(args[-len(defaults):], defaults))
        depends = defaults.get(DEPEND, [])
        if inspect.isfunction(depends):
            depends = [depends]
        elif not isinstance(depends, Iterable):
            raise ValueError(function.__name__ + "'s dependencies were not understood.")
        @wraps(func)
        def func_bundle(*args, **kwargs):
            for depend in depends:
                depend()
            return func(*args, **kwargs)
        pymake.__setattr__(f, func_bundle)

    if DEPEND in args:
        args.remove(DEPEND)
    for arg in args:
        subparser.add_argument(arg)
    subparser.set_defaults(handler = pymake.__getattribute__(f))
    # TODO effectively handle keywords and defaults
 
def main()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    for f in functions:
        add_function(subparsers, f)
   
    if len(sys.argv) < 2:
        args = parser.parse_args(['all'])
    else:
        args = parser.parse_args()
        
    kwargs = vars(args)
    function = args.handler
    del kwargs['handler']
    function(**kwargs)
