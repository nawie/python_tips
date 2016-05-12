# get date like php format
#
# example   : date('d-M-Y'), minus 1 day date('d-M-Y', -1), plus 1 day date('d-M-Y', 1)
# result    : 12-05-2016, 11-05-2016, 13-05-2016,
#
import datetime, re
def date(format = "", delta = 0):
    assert isinstance(format, basestring), "Date format must be a string"
    assert isinstance(delta, int), "Date delta must be an integer"
    if not format :
        format = 'Y-m-d H:M:S'
    # check date part
    def part(x):
        return '%'+x if re.match("[^\W\d_]",x) else x
    # check is delta
    now = datetime.datetime.now() + datetime.timedelta(days=delta)
    # result
    return now.strftime(
            ''.join(map(part, format))
        )
