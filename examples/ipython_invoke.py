from random import random

def all():
    x = [random() for _ in range(10)]
    import IPython()
    IPython.embed()

