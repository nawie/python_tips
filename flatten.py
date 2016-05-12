# flatten inline list into single list
#
# example   : flatten(['FIRST', 'SECOND', ['THIRD', 'FOURTH']])
# result    : ['FIRST', 'SECOND', 'THIRD', 'FOURTH']
#
def flatten(*args):
    flatten = lambda *args: (result for mid in args for result in (flatten(*mid) if isinstance(mid, (tuple, list)) else (mid,)))
    return list(flatten(*args))