# Depends Proposals
# seems like there need to be two ways of defining things, one with function calls
# and one with function definitions. Function definitions are far and away the most
# natural way to define actions (data point 1: every existing build tool does it like that)
# but directory and file names and rules can't be expressed as function names (`.c` is not a valid
# python function.
# 
# and everything can't be a function call since python doesn't have multi-line lambdas, and function def
# + function call for every rule seems very excessive.
# 
# There is another way to think about things, which I think holds.
# Any function-def is a phony task (in the Makefile sense of phony - there's no check that the target
# is up to date. Any function-rule one is not a phony task. 
# 
# In any case, the best solution, then, is to find the most natural (and ideally similar) way to do things for
# both rule definitions.
# 
# Function Call Proposals
# 1
directory("/foo/bar/")
depends("/foo/bar", "hello")
# 2
file("hello").depends("one", "two", "three")
# 3
file("hello", depends="foo")

# Function Definition Proposals
# 1
@ignore
@depends(foobar)
def command(arg1):
    print arg1
# + very pythonic
# + easy to read
# - first column could get cluttered if we have to throw these everywhere

# 2
def command(arg1, depends="foo"):
    print arg1
# - weird syntax
# + first column stays clean
# - confusing to revisit

# 3
def command(arg1):
    depends("foo")
# - very unpythonic
# + first column stays clean
# - doesn't behave like normal body of function

# 4
def command(arg1) -> [dep1, dep2]:
    pass
# + exactly the same as Rake (even if interpreted by language in totally different way)
# - doesn't work in python2 
# + first column stays clean
# + easy to read

# Conclusion
# I really only like proposal 3 for the Function Calls, and two and four seem nicest for Function
# Definition. 4 is tempting, but it seems a major negative that its python3 only. On the other hand,
# maybe thats a forcing function to update to Python3...
