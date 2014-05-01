@ignore
def helper():
    print 'helping'

def clean():
    """Clean shit. """
    print 'cleaning'

@depends(clean)
def build():
    """Build shit. """
    print 'building'

all=build
