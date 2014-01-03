from pymake import *

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
