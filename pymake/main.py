from logging import basicConfig, DEBUG, INFO, debug, info
from functools import wraps
import argparse
import inspect
import pymake
import imp
import sys
import os
from api import env
from task import Task, rules

def add_function(subparsers, module, funcname):
    func = getattr(module, funcname)
    if getattr(func, 'ignore', False) or not inspect.isfunction(func):
        return

    subparser = subparsers.add_parser(funcname, help=func.__doc__)
    args, varargs, keywords, defaults = inspect.getargspec(func)
    defaults = defaults or []
    n_defaults = len(defaults)

    for arg in args[:-n_defaults]:
        subparser.add_argument(arg)
    for arg, default in zip(args[-n_defaults:], defaults):
        name = ('-' if len(arg) == 1 else '--') + arg
        if isinstance(default, bool):
            action = "store_" + str(not default).lower()
            subparser.add_argument(name, default=default, action=action)
        elif isinstance(default, int):
            subparser.add_argument(name, default=default,
                    action="store", type=int)
        else:
            subparser.add_argument(name, default=default,
                    action="store")

    depends = getattr(func, "depends", None)
    rules[funcname] = Task(funcname, func, depends)


def find_pymake_file():
    fnames = [
        "Pymake",
        "pymake",
        "Pymake.py",
        "pymake.py",
    ]
    found = ""
    for fname in fnames:
        if os.path.exists(fname):
            debug("found: %s", fname)
            found = os.path.abspath(fname)
            break
    return found
 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', action="store_true", default=False,
        dest='pymake_D',
        help="Debug output.")

    subparsers = parser.add_subparsers(dest="subparser")

    command_mod = imp.new_module('command_mod')
    dummy_mod = imp.new_module('dummy_mod')

    pkg_path = os.path.dirname(pymake.__file__)
    api_code = compile("from pymake.api import *", pkg_path+"/api.py", "exec")
    exec(api_code, dummy_mod.__dict__)
    exec(api_code, command_mod.__dict__)

    pymake_file = find_pymake_file()
    if not pymake_file:
        print 'No Pymake file found. Exiting...'
        return

    with open(pymake_file) as f:
        code = f.read()
    user_code = compile(code, pymake_file, "exec")
    exec(user_code, command_mod.__dict__)
    
    functions = [f for f in dir(command_mod) if f not in dir(dummy_mod)]

    for f in sorted(functions):
        add_function(subparsers, command_mod, f)
   
    if len(sys.argv) < 2:
        args = parser.parse_args([env.DEFAULT_ACTION])
    else:
        args = parser.parse_args()

    basicConfig(level=DEBUG if args.pymake_D else INFO)
    debug("Tasks found: %s", sorted(rules.keys()))
    debug("Passed command line arguments: %s", args)
    command = args.subparser
    kwargs = vars(args)
    del kwargs['subparser']
    del kwargs['pymake_D']

    rules[command].run(**kwargs)

