# php like explode for python
#
# example   : explode('FIRST|SECOND|THIRD:FOURTH', '|:')
# result    : ['FIRST', 'SECOND', 'THIRD', 'FOURTH']
#
def explode(text , separator = '/@'):
    if isinstance(text, basestring):
        def transform(sequence, char):
            def split(subsequence, substack):
                subsequence.extend(filter(lambda _text: _text != '', substack.split(char)))
                return subsequence
            return text.split(char) if not sequence else reduce(split, sequence, [])
        return reduce(transform, separator, [])
    else:
        return None