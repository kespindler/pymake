from collections import Iterable, Mapping
from logging import debug
import api
#from api import env

rules = {}

class Task:
    def __init__(self, name, action, depends=None):
        self.name = name
        self.action = action
        self.depends = []
        self.executed = False
        self.args = [] # list of varnames of the args
        self.varargs = None # variable name of the varargs
        self.kwargs = None
        self.defaults = {}
        if depends is not None:
            if (isinstance(depends, basestring) or 
                not isinstance(depends, Iterable)):
                depends = [depends]
            for d in depends:
                if isinstance(d, basestring):
                    self.depends.append(d)
                else:
                    self.depends.append(d.__name__)

    def run(self, cmd_args):
        debug('Running: %s', self.name)
        debug('Depends: %s', self.depends)
        if self.executed:
            debug('%s has already executed. Skipping.', self.name)
            return None
        for task in self.depends:
            action = rules[task]
            # build args here.
            action.run(cmd_args)
        if callable(self.action):
            args, kwargs = self.build_args(cmd_args)
            debug("Signature: arg: %s, var: %s, kwarg: %s, default: %s)",
                    self.args, self.varargs, self.kwargs, self.defaults)
            debug("args: %s", args)
            debug("kwargs: %s", cmd_args)
            self.action(*args, **kwargs)
        elif self.action is not None:
            function = api.env.DEFAULT_INTERP
            # TODO do i need to rethink this signature?
            function(self.action, self.name)
        self.executed = True

    def build_args(self, cmd_args):
        args = []
        kwargs = {}  # unused
        for arg in self.args:
            if arg in cmd_args:
                value = cmd_args[arg]
            elif arg in self.defaults:
                value = self.defaults[arg]
            else:
                raise TypeError("arg %s not passed "
                        "in and has no default for task %s." %
                        (arg, self.name))
            args.append(value)
        if self.varargs:
            args.extend(cmd_args[self.varargs])
        return args, kwargs

