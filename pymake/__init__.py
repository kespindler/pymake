"""
from api import *

def main()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    for f in functions:
        add_function(subparsers, f)
   
    if len(sys.argv) < 2:
        args = parser.parse_args(['all'])
    else:
        args = parser.parse_args()
        
    kwargs = vars(args)
    function = args.handler
    del kwargs['handler']
    function(**kwargs)


"""
from api import *

env = Environment()
rules = {} # mapping from string or function to 

