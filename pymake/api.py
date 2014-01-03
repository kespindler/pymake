from collections import Iterable
from functools import partial, wraps
import argparse
import inspect
import sys
import imp
import os
import re
from logging import basicConfig, DEBUG, INFO, debug, LogRecord

def getMessage(self):
    msg = str(self.msg)
    print msg
    if self.args:
        msg = msg.format(*self.args)
    print msg
    return msg
LogRecord.getMessage = getMessage

#basicConfig(level=DEBUG)
basicConfig()

rules = {} # mapping from string or function to 

class SystemError(Exception):
    pass

class Action:
    def __init__(self, name, action, depends=None):
        self.name = name
        self.action = action
        self.depends = []
        if depends is not None:
            if not isinstance(depends, Iterable):
                depends = [depends]
            for d in depends:
                if isinstance(d, basestring):
                    self.depends.append(d)
                else:
                    self.depends.append(d.__name__)

    def run(self, *args, **kwargs):
        debug('Running {}', self.name)
        debug('Depends {}', self.depends)
        for task in self.depends:
            action = rules[task]
            action.run(*args, **kwargs)
        if callable(self.action):
            self.action(*args, **kwargs)
        elif self.action is not None:
            function = env.DEFAULT_INTERP
            arg = FileFormatObject(self.name)
            function(self.action, arg)

def directory(dir, depends=None):
    """Register a file task where the action is mkdir. 

    :param dir: the directory path as a string.
    :param depends: a dependency or list of dependencies.

    Usage::

      # Upon rule's execution, will create a new directory at this location
      >>> directory("/my/directory/path")
    """
    file(dir, action = "mkdir " + dir, depends=depends)

def file(fpath, action=None, depends=None):
    """Register a task corresponding to the file fpath. Will only be built if file must be updated.
    An action can be either a string or a callable. If it is a string, it will be passed to the env's
    DEFAULT_INTERP function and therefore follows same conventions as the `sh` command ({}-style
    format, 

    :param fpath: the file path.
    :param action: string or callable. String is executed by the default interpreter.
    :param depends: a dependency or list of dependencies.
    """
    rules[fpath] = Action(fpath, action, depends)

def rule(matcher, action=None, depends=None):
    """Register a rule-based task. If passed a compiled regex object, it will work according to that
    object. Otherwise, it will be assumed to be a file ending.

    :param matcher: file-ending string or compiled regex.
    """
    if isinstance(matcher, basestring):
        matcher = re.compile("[^/?*:;{}\\]+"+matcher+"$")
    rules[fpath] = Action(fpath, action, depends)
    
def depends(*args):
    """Decorator to create dependencies for a rule. 
    """
    def depends_closure(func):
        depends = getattr(func, 'depends', [])
        depends.extend(args)
        func.depends = depends
        return func
    return depends_closure

def ignore(func):
    """Decorator to not create a command-line command for a rule.
    """
    func.ignore = True
    return func

# Only used when the formatting actually starts to occur
class FileFormatObject:
    def __init__(self, fpath):
        self.fpath = fpath
        self.basename = os.path.basename(fpath)
        self.name = os.path.splitext(fpath)[0]

    def __str__(self):
        return self.fpath

def sh(format_cmd, t=None):
    """Accepts a new-style (with {}) Python format string, and executes it as a shell command.
    If no object for formatting is given, we use some Python magic to extract the first arg of the
    calling function.
    """
    if t is None:
        cur_frame = inspect.currentframe()
        caller_frame = cur_frame.f_back
        #fpath = caller_frame.f_locals["__fname"]
        args = caller_frame.f_code.co_varnames
        if len(args):
            fpath = caller_frame.f_locals[args[0]]
            t = FileFormatObject(fpath)

    if t is None: # no arg was found
        cmd = format_cmd
    else:
        cmd = format_cmd.format(t, **vars(t))
    code = os.system(cmd)
    if code:
        raise SystemError("Command finished with non-zero return value.")

def pymake(taskname, *args, **kwargs):
    """ Calls execution of a task. Use this if the task you'd like to execute cannot be expressed as a
    Python object name (e.g. it is a filepath).

    # Executes the task for /my/file
    >>> pymake.pymake("/my/file")
    """
    action = rules[taskname]
    action.run(*args, **kwargs)

def add_function(subparsers, module, f):
    func = getattr(module, f)
    if getattr(func, 'ignored', False) or not inspect.isfunction(func):
        return

    # TODO effectively handle keywords and defaults
    subparser = subparsers.add_parser(f, help=func.__doc__)
    args, varargs, keywords, defaults = inspect.getargspec(func)
    for arg in args:
        subparser.add_argument(arg)

    depends = getattr(func, "depends", None)

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        action = rules[f]
        action.run(*args, **kwargs)

    #func_partial = partial(pymake, taskname=f)
    setattr(module, f, func_wrapper)
    rules[f] = Action(f, func, depends)
 
def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser")

    pymake = imp.new_module('pymake')
    dummy = imp.new_module('dummy')

    exec "from pymake import *" in dummy.__dict__

    fnames = ["Pymake",
            "pymake",
            "Pymake.py",
            "pymake.py"]
    for fname in fnames:
        if not os.path.exists(fname):
            continue
        with open(fname) as f:
            code = f.read()
        break
    try:
        exec code in pymake.__dict__
    except NameError:
        info('No Pymake file found. Exiting...')
        return
    
    functions = [f for f in sorted(dir(pymake)) if f not in dir(dummy)]

    debug("functions found {}", functions)
    for f in functions:
        add_function(subparsers, pymake, f)
   
    if len(sys.argv) < 2:
        args = parser.parse_args([env.DEFAULT_ACTION])
    else:
        args = parser.parse_args()
        
    debug("args {}", args)
    command = args.subparser
    kwargs = vars(args)
    del kwargs['subparser']

    rules[command].run(**kwargs)

class Environment:
    """Specifies some defaults for Pymake. Specifically,
    :param DEFAULT_INTERP: the command to which string commands will be passed.
    :param DEFAULT_ACTION: when pymake is invoked without a subcommand, this task will be invoked.
    """
    def __init__(self):
        self.DEFAULT_INTERP = sh
        self.DEFAULT_ACTION = "all"
    pass

env = Environment()
