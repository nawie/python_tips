# Public Domain, i.e. feel free to copy/paste
# Considered a hack in Python 2
# Based on https://gist.github.com/techtonik/2151727

import sys
import inspect

def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method
    
       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.
       
       An empty string is returned if skipped levels exceed stack height
    """
    name  = []
    limit = iter(xrange(1, skip + 1))
    frame = sys._getframe(1)

    try:
        while frame and next(limit):
            frame = frame.f_back
            
    except StopIteration:
        parent_frame = frame
    else:
        return ''

    module = inspect.getmodule(parent_frame)
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parent_frame.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parent_frame.f_locals['self'].__class__.__name__)
    codename = parent_frame.f_code.co_name
    # top level usually
    if codename != '<module>':
        name.append(codename) # function or a method
    del frame, parent_frame, limit
    return ".".join(name)

if __name__ == '__main__':
            
    class base(object):
        
        def error(self, error, frame = 2):
            print('Error:{method}:{error}({message})'.format(method = caller_name(frame), error=error.__class__.__name__, message = error.message))
            
            
    class child(base):
        
        def message(self, message = None):
            try:
                raise ValueError(message)
            except Exception as e:
                self.error(e, 1)
            
            
    def test():
        data = child()        
        data.message('error on value')

    test()

#   >>> Error:child.message:ValueError(error on value)
