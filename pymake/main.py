from logging import DEBUG, INFO, debug, info, getLogger
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
    depends = getattr(func, "depends", None)
    task = Task(funcname, func, depends)
    rules[funcname] = task

    subparser = subparsers.add_parser(funcname, help=func.__doc__)
    args, varargs, keywords, defaults = inspect.getargspec(func)
    defaults = defaults or []
    args = args or []
    n_args = len(args) - len(defaults)
    for arg in args[:n_args]:
        subparser.add_argument(arg)
        task.args.append(arg)
    if varargs:
        subparser.add_argument(varargs,
                nargs="*")
        task.varargs = varargs
    for arg, default in zip(args[n_args:], defaults):
        task.args.append(arg)
        task.defaults[arg] = default
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
 

def pop_pymake_args(args, pymake_args):
    command = args.subparser
    kwargs = vars(args)
    del kwargs['subparser']
    for k in pymake_args:
        dest = pymake_args[k]['dest']
        del kwargs[dest]
    return command, kwargs


def main():
    parser = argparse.ArgumentParser()
    pymake_args = {
        'D': dict(action="store_true",
             default=False,
             help='Debug output.'),
        'cold': dict(action="store_true", 
             default=False,
             help="Cold run shell output."),
    }
    for k in pymake_args:
        pymake_args[k]['dest'] = "pymake_" + k
        arg = '-'*(1 if len(k)==1 else 2) + k
        parser.add_argument(arg, **pymake_args[k])
    subparsers = parser.add_subparsers(dest="subparser")

    command_mod = imp.new_module('command_mod')
    dummy_mod = imp.new_module('dummy_mod')
    sys.modules['command_mod'] = command_mod

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

    getLogger().setLevel(level=DEBUG if args.pymake_D else INFO)
    env.COLD = args.pymake_cold

    debug("Tasks found: %s", sorted(rules.keys()))
    debug("Passed command line arguments: %s", args)

    command, kwargs = pop_pymake_args(args, pymake_args)
    task = rules[command]
    task.run(kwargs)

