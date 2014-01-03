import inspect

def caller(b, c, d):
    a = 5
    callee()

def callee():
    cur_frame = inspect.currentframe()
    outer_frames = inspect.getouterframes(cur_frame)
    caller_frame = outer_frames[1][0]
    print caller_frame

    first_arg = caller_frame.f_code.co_varnames[0]
    first_argval = caller_frame.f_locals[first_arg]
    print first_arg, first_argval

caller(1,2,3)
