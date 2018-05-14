import multiprocessing

from Queue import Empty
from inspect import getargspec as signature

try:
    import dill
except ImportError:
    pass

__all__ = ['timeout', 'TimeoutError']

class TimeoutError(Exception):
    pass

class timeout(object):
    def __init__(self, using_dill=False, raise_error=False):
        self.using_dill = using_dill
        self.raise_error = raise_error

    @staticmethod
    def container(queue, payloads, using_dill=False):
        try:
            if using_dill:
                func, args, kwargs = dill.loads(payloads)
            else:
                func, args, kwargs = payloads
        except Exception as e:
            result = e
        else:
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                result = e
        finally:
            queue.put(result)

    def __call__(self, func, args=(), kwargs={}, timeout=1, default=None, raise_error=None):
        multiprocessing.freeze_support()

        if self.using_dill:
            payloads = dill.dumps((func, args, kwargs))
        else:
            payloads = func, args, kwargs

        queue       = multiprocessing.Queue()
        process     = multiprocessing.Process(target = self.__class__.container, args = (queue, payloads, self.using_dill))
        result      = default
        raise_error = raise_error if isinstance(raise_error, bool) else self.raise_error

        try:
            process.start()
            result = queue.get(block=True, timeout=timeout)
        except Empty:
            process.terminate()
            if hasattr(func, '__name__'):
                message = 'Method:{func_name}-{func_args}'.format(func_name=func.__name__, func_args=signature(func))
            else:
                message = 'Method:{func_obj}'.format(func_obj=func)
            result = TimeoutError('{message}, Timeout:{time}\'s'.format(message=message, time=timeout))
        finally:
            queue.close()
            process.join()
            if isinstance(result, Exception):
                if raise_error:
                    raise result  # pylint: disable=E0702
                return default
            return result

if __name__ == '__main__':
    import time

    def foo(x=1):
        cnt = 1
        while True:
            time.sleep(1)
            print(x, cnt)
            cnt += 1

    print(timeout()(foo, kwargs={'x': 'Hi'}, timeout=3, default='Bye'))
    print(timeout()(foo, args=(2,), timeout=2, default='Sayonara'))
    print(timeout()(foo, args=(2,), timeout=2, raise_error=True))
    """
    >>> ('Hi', 1)
    >>> ('Hi', 2)
    >>> Bye
    >>> (2, 1)
    >>> Sayonara
    >>> (2, 1)
    >>> Traceback (most recent call last):
        File "timeout.py", line 82, in <module>
            print(timeout()(foo, args=(2,), timeout=2, raise_error=True))
        File "timeout.py", line 66, in __call__
            raise result  # pylint: disable=E0702
        __main__.TimeoutError: Method:foo-ArgSpec(args=['x'], varargs=None, keywords=None, defaults=(1,)), Timeout:2's
    """
