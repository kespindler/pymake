
class Environment:
    """Specifies some defaults for Pymake. Specifically,
    :param DEFAULT_INTERP: the command to which string commands will be passed.
    :param DEFAULT_ACTION: when pymake is invoked without a subcommand, this task will be invoked.
    """
    def __init__(self):
        self.DEFAULT_INTERP = sh
        self.DEFAULT_ACTION = all
    pass

env = Environment()

def directory(dir, depends=None):
    """Register a file task where the action is mkdir. 

    :param dir: the directory path as a string.

    Usage::

      # Upon rule's execution, will create a new directory at this location
      >>> directory("/my/directory/path")
    """
    file(dir, action = "mkdir " + dir)

def file(fpath, action=None, depends=None):
    """Register a task corresponding to the file fpath. Will only be built if file must be updated.
    An action can be either a string or a callable. If it is a string, it will be passed to the env's
    DEFAULT_INTERP function and therefore follows same conventions as the `sh` command ({}-style
    format, 

    :param fpath: the file path.
    :param action: string or callable. String is 
    """

def rule(matcher, action=None, depends=None):
    """Register a rule-based task. If passed a compiled regex object, it will work according to that
    object. Otherwise, it will match using endswith (for file endings).

    :param matcher: file-ending string or compiled regex.
    """
    
def depends(*args):
    """Decorator to create dependencies for a rule. 
    """
    def depends_closure(func):
        func.depends = args
        return func
    return depends_closure

def ignore(func):
    """Decorator to not create a command-line command for a rule.
    """
    func.ignore = True
    return func

def sh(format_cmd, t=None):
    """Accepts a new-style (with {}) Python format string, and executes it as a shell command.
    If no object for formatting is given, we use some Python magic to extract the first arg of the
    calling function.
    """
    cmd = format_cmd.format(t, **vars(t))
    os.system(cmd)

def pymake(taskname):
    """ Calls execution of a task. Use this if the task you'd like to execute cannot be expressed as a
    Python object name (e.g. it is a filepath).

    # Executes the task for /my/file
    >>> pymake.pymake("/my/file")
    """

############################
# Example
############################

# Create rule for directory /foo/bar
directory("/foo/bar/")

# Create rule for creating "hello"
# When invoked, it first looks for a file-rule `/foo/bar`, executes it, and then 
# calls the `action` string in the terminal.
file("hello", action = "cc -o {0} {0}.c", depends="/foo/bar")
file("hello", action = "cc -o hello hello.c", depends="/foo/bar")

# This creates a helper function `helper`, which can be used entirely normally.
# The ignore simply means that no terminal command is created for it.
@ignore
def helper(arg1):
    print arg1

# This creates a terminal command `command`, which will take a single argument.
# Before its execution, it will execute the function `foobar`
@depends(foobar)
def command(arg1):
    print arg1

# Each of these following functions will also be turned into terminal commands.
# Note, however, 
def clean():
    sh("rm -rf build")

def cc(t):
    sh("cc -o {name} {source}")

def all():
    """The default task.
    """
    clean()
    pymake("hello")

@depends(clean, "hello")
def all2():
    """Does the same thing as `all`.
    """
