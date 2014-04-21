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
        if depends is not None:
            if (isinstance(depends, basestring) or 
                not isinstance(depends, Iterable)):
                depends = [depends]
            for d in depends:
                if isinstance(d, basestring):
                    self.depends.append(d)
                else:
                    self.depends.append(d.__name__)

    def run(self, *args, **kwargs):
        debug('Running: %s', self.name)
        debug('Depends: %s', self.depends)
        if self.executed:
            debug('%s has already executed. Skipping.', self.name)
            return None
        for task in self.depends:
            action = rules[task]
            action.run(*args, **kwargs)
        if callable(self.action):
            self.action(*args, **kwargs)
        elif self.action is not None:
            function = api.env.DEFAULT_INTERP
            function(self.action, self.name)
        self.executed = True

