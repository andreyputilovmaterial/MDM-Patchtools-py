

import re




class PatchException(Exception):
    """Error"""
class PatchInsertException(PatchException):
    """Error"""
class PatchFindPositionException(PatchException):
    """Error"""




def find_position(pattern,txt):
    if isinstance(pattern,list):
        last_er = None
        for attempt in pattern:
            try:
                return find_position(attempt,txt)
            except Exception as e:
                last_er = e
        raise last_er
    elif isinstance(pattern,int):
        if pattern>=0:
            return pattern
        elif pattern<0:
            return len(txt) + pattern + 1
        else:
            raise PatchFindPositionException('patch: find_position: assert: int is not >=0 and not <0, what is it? ("{pattern}")'.format(pattern=pattern))
    elif isinstance(pattern,re.Pattern):
        regex_matches = re.finditer(pattern,txt)
        if not regex_matches:
            return None
        captured_group_num = 1
        # we expect that pattern includes 2 gropus, and we add something in between
        # even if something is not captured in between those 2 groups, we don't delete it
        # so this is kind of extraneous
        # but this syntax makes it clear, we are adding after the first group before the second one, so that it's not confusing if we are adding before or after the regex
        # and, to re-iterate on this, we are only adding, we are not replacing/modyfying it somehow with a regex
        regex_match = [m for m in regex_matches][0]
        _, pos = regex_match.span(captured_group_num)
        return pos
    elif not pattern:
        return 0
    elif isinstance(pattern,dict):
        assert 'type' in pattern, 'trying to find a position in text, and the position is specified as dict but position[type] is missing ({pattern})"'.format(pattern=pattern)
        pattern_type = pattern['type']
        if pattern_type=='custom':
            return find_position(pattern['payload'],txt)
        elif pattern_type=='none':
            return find_position(None,txt)
        elif pattern_type=='address':
            raise PatchFindPositionException('trying to find a position in text, and the position is specified as text: we can\'t do that ({pattern}, type={t})"'.format(pattern=pattern,t=pattern['type']))
        elif pattern_type=='position':
            return find_position(pattern['position'],txt)
        elif pattern_type=='re':
            pattern_re=re.compile(pattern['pattern'],flags=pattern['flags'] if 'flags' in pattern else None)
            return find_position(pattern_re,txt)
        else:
            raise PatchFindPositionException('trying to find a position in text, and the position is specified as dict but not of any recognized format: we can\'t do that ({pattern}, type={t})"'.format(pattern=pattern,t=pattern['type']))
    else:
        raise PatchFindPositionException('can\'t parse and find position ({pattern})"'.format(pattern=pattern))


def find_position_span(pattern,txt):
    if isinstance(pattern,list):
        last_er = None
        for attempt in pattern:
            try:
                return find_position_span(attempt,txt)
            except Exception as e:
                last_er = e
        raise last_er
    elif isinstance(pattern,dict):
        assert 'type' in pattern, 'trying to find a position in text, and the position is specified as dict but position[type] is missing ({pattern})"'.format(pattern=pattern)
        pattern_type = pattern['type']
        if pattern_type=='re':
            pattern_re=re.compile(pattern['pattern'],flags=pattern['flags'] if 'flags' in pattern else None)
            return find_position_span(pattern_re,txt)
        else:
            raise PatchFindPositionException('Patch: find_position_span: position must be regex, or list of regex\'s ({pattern})"'.format(pattern=pattern))
    elif isinstance(pattern,re.Pattern):
        regex_matches = re.finditer(pattern,txt)
        if not regex_matches:
            raise PatchFindPositionException('Patch: find_position_span: position not found ({pattern})"'.format(pattern=pattern))
        captured_group_num = 0
        regex_matches = [m for m in regex_matches]
        if not (len(regex_matches)>0):
            raise PatchFindPositionException('Patch: find_position_span: position not found ({pattern})"'.format(pattern=pattern))
        regex_match = regex_matches[0]
        return regex_match.span(captured_group_num)
    else:
        raise PatchFindPositionException('Patch: find_position_span: position must be regex, or list of regex\'s ({pattern})"'.format(pattern=pattern))





class PatchInsert():

    handled_action = 'insert'

    def __init__(self,txt):
        self.txt = txt

    def __call__(self, chunk):
        
        def what_to_add(chunk):
            txt = None
            if isinstance(chunk['payload'],dict):
                txt = chunk['payload']['lines']
            else:
                txt = chunk['payload']
            txt = '{t}'.format(t=txt) # ensure it's text
            return txt

        def where_to_add(chunk,txt):
            return find_position(chunk['position'],txt)
        
        txt = what_to_add(chunk)
        pos = where_to_add(chunk,self.txt)
        yield { 'op': 'add', 'text': txt, 'pos': pos }


        
class PatchReplace():

    handled_action = 'replace'

    def __init__(self,txt):
        self.txt = txt

    def __call__(self, chunk):
        
        def what_to_add(chunk):
            txt = None
            if isinstance(chunk['payload'],dict):
                txt = chunk['payload']['lines']
            else:
                txt = chunk['payload']
            txt = '{t}'.format(t=txt) # ensure it's text
            return txt

        txt = what_to_add(chunk)
        pos_skip = 0
        pos_begin, pos_end = find_position_span(chunk['position'],self.txt[pos_skip:])
        yield { 'op': 'remove', 'del': pos_end-pos_begin, 'pos': pos_begin + pos_skip }
        yield { 'op': 'add', 'text': txt, 'pos': pos_end + pos_skip }
        while True:
            try:
                pos_skip = pos_skip + pos_end
                pos_begin, pos_end = find_position_span(chunk['position'],self.txt[pos_skip:])
                yield { 'op': 'remove', 'del': pos_end-pos_begin, 'pos': pos_begin + pos_skip }
                yield { 'op': 'add', 'text': txt, 'pos': pos_end + pos_skip }
                if pos_skip==pos_end:
                    assert False # separate line, so that I can put a breakpoint here
            except PatchFindPositionException:
                break






