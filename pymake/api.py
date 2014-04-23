from collections import Iterable, Mapping
from functools import partial, wraps
from logging import debug, info
from exceptions import OSError
import task
import sys
import os
import re
import sys

def directory(dir, depends=None):
    """Register a file task where the action is mkdir. 

    :param dir: the directory path as a string.
    :param depends: a dependency or list of dependencies.

    Usage::

      # Upon rule's execution, will create a new directory at this location
      >>> directory("/my/directory/path")
    """
    file(dir, "mkdir '%s'" % dir, depends)

def file(fpath, action, depends=None):
    """Register a task corresponding to the file fpath. Will only be built if file must be updated.
    An action can be either a string or a callable. If it is a string, it will be passed to the env's
    DEFAULT_INTERP function and therefore follows same conventions as the `sh` command ({}-style
    format, 

    :param fpath: the file path.
    :param action: string or callable. String is executed by the default interpreter.
    :param depends: a dependency or list of dependencies.
    """
    task.rules[fpath] = task.Task(fpath, action, depends)

def rule(matcher, action=None, depends=None):
    """Register a rule-based task. If passed a compiled regex object, it will work according to that
    object. Otherwise, it will be assumed to be a file ending.

    :param matcher: file-ending string or compiled regex.
    """
    if isinstance(matcher, basestring):
        matcher = re.compile("[^/?*:;{}\\]+"+matcher+"$")
    task.rules[fpath] = task.Task(fpath, action, depends)
    
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

def sh(cmd_fstring, args = None):
    if args is None:
        cur_frame = sys._getframe()
        back_frame = cur_frame.f_back
        args = back_frame.f_globals.copy()
        args.update(back_frame.f_locals)

    fmtdict = {}
    if isinstance(args, Mapping):
        fmtdict.update(args)
    elif hasattr(args, "__dict__"):
        fmtdict.update(vars(args))
    cmd = cmd_fstring.format(args, **fmtdict)
    if env.COLD:
        info(cmd)
    else:
        debug(cmd)
        code = os.system(cmd)
        if code:
            raise OSError("Command finished with non-zero return value.")


class Environment:
    """Specifies some defaults for Pymake. Specifically,
    :param DEFAULT_INTERP: the command to which string commands will be passed.
    :param DEFAULT_ACTION: when pymake is invoked without a subcommand, this task will be invoked.
    """
    def __init__(self):
        self.DEFAULT_INTERP = sh
        self.DEFAULT_ACTION = "all"
        self.COLD = False
    pass

env = Environment()

