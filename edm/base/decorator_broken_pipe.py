from functools import wraps
from sys import exit, stderr, stdout
from traceback import print_exc



def suppress_broken_pipe_msg(f):
    """
    装饰器 解决broken_pipe
    :param f:
    :return:
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except SystemExit:
            raise
        except:
            print_exc()
            exit(1)
        finally:
            try:
                stdout.flush()
            finally:
                try:
                    stdout.close()
                finally:
                    try:
                        stderr.flush()
                    finally:
                        stderr.close()
    return wrapper


