
def runfirst(task=5):
    print 'runfirst', task

@depends(runfirst)
def example(farg1, foo=False, bar="", *fargs):
    print farg1
    print fargs
    print foo
    print bar

