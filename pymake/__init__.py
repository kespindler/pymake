from pymake.main import main
import task
__version__ = "0.1"

def pymake(taskname, *args, **kwargs):
    """ Calls execution of a task. Use this if the task you'd like to execute cannot be expressed as a
    Python object name (e.g. it is a filepath).

    # Executes the task for /my/file
    >>> pymake.pymake("/my/file")
    """
    cur_task = task.rules[taskname]
    cur_task.run(*args, **kwargs)

