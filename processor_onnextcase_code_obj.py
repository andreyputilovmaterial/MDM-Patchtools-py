
import re





CONFIG_NUMLINEBREAKS_INBETWEEN = 2
CONFIG_NUMLINEBREAKS_AROUND = 0




class CodeNode:
    def __init__(self,scripts,substitutions_for_children):
        self._scripts = scripts
        self._substitutions_for_children = substitutions_for_children
        self._children = []
    
    def add(self,nested):
        self._children.append(nested)
    
    # def __str__(self):
    # we can't use __str__ because we need some parameters passed from parent level
    def render(self,substitutions):
        # actually, rendering
        # the most interesting part goes here
        def find_regex_span(regex,text,captured_group_num=0,re_flags=re.I|re.DOTALL):
            # maybe having this fn is not totally right
            # python offers everything to work with regexs, and I am developing a different hack to work with regexs differently...
            # anyway, workling like this is easier for me
            # I am not just doing replacements, that might work, or might not work
            # I am finding exact position of found sequence and doing string concatenation
            find_regex_results = re.finditer(regex,text,flags=re_flags)
            if not find_regex_results:
                raise ValueError('searching for pattern failed')
            return [m for m in find_regex_results][0].span(captured_group_num)
        def trim_lines(s):
            if re.match(r'^\s*$',s):
                return ''
            s = re.sub(r'(^\s*(?:\s*?\n)*\n)(.*?$)',lambda m: m[2],s,flags=re.DOTALL)
            s = re.sub(r'(^.*?\n)(\s*(?:\s*?\n)*$)',lambda m: m[1],s,flags=re.DOTALL)
            return s
        def add_indent(s,indent):
            # s = '\n'+s # I am adding a line break at the beginning to make wotking with regexs easier
            # s = re.sub(r'(\n)',lambda m: '{k}{i}'.format(i=indent,k=m[1]),s)
            # s = s[1:] # remove line break at the beginning that we added
            # return s
            if s[-1]=='\n':
                s = s[:-1]
                s = re.split(r'\n',s,flags=re.I|re.DOTALL)
                s = [indent+p for p in s]
                s = '\n'.join(s)
                s = s + '\n'
            else:
                s = re.split(r'\n',s,flags=re.I|re.DOTALL)
                s = [indent+p for p in s]
                s = '\n'.join(s)
            return s
                
        code_to_add = self._scripts
        code_to_add = code_to_add.replace('<<VAR_LVALUE_PATH>>',substitutions['variable_lvalue_path']).replace('<<VAR_RVALUE_PATH>>',substitutions['variable_rvalue_path'])
        if len(self._children)>0:
            # code_to_add = trim_lines(code_to_add) # why?
            code_to_add = '\n' + code_to_add
            nested_code_marker_span = find_regex_span(r'(?:^|\n)([^\S\r\n]*?)(\'\s*\{@\})(\s*?\n)',code_to_add)
            code_to_add_part_leading = (code_to_add[:nested_code_marker_span[0]] + '\n')[1:]
            code_to_add_part_trailing = code_to_add[nested_code_marker_span[1]:]
            code_to_add_marker = code_to_add[nested_code_marker_span[0]:nested_code_marker_span[1]]
            indent_span = find_regex_span(r'^\n?(\s*)\'',code_to_add_marker,captured_group_num=1)
            indent = code_to_add_marker[indent_span[0]:indent_span[1]]
            assert not '\n' in indent
            newline_between_items = '{s}{n}'.format(s=indent,n='\n')
            return '{part_begin}{part_subfields}{part_end}'.format(
                part_begin = code_to_add_part_leading, # trim_lines(code_to_add_part_leading),
                part_end = code_to_add_part_trailing, # trim_lines(code_to_add_part_trailing),
                part_subfields = newline_between_items*CONFIG_NUMLINEBREAKS_AROUND+(newline_between_items*CONFIG_NUMLINEBREAKS_INBETWEEN).join([ trim_lines('{subfield_code}'.format(subfield_code=trim_lines(add_indent(subfield.render(self._substitutions_for_children),indent)))) for subfield in self._children ])+newline_between_items*CONFIG_NUMLINEBREAKS_AROUND,
            )
        else:
            # code_to_add = trim_lines(code_to_add) # why?
            code_to_add = '\n' + code_to_add
            nested_code_marker_span = find_regex_span(r'(?:^|\n)([^\S\r\n]*?)(\'\s*\{@\})(\s*?\n)',code_to_add)
            code_to_add_part_leading = (code_to_add[:nested_code_marker_span[0]] + '\n')[1:]
            code_to_add_part_trailing = code_to_add[nested_code_marker_span[1]:]
            return code_to_add_part_leading + code_to_add_part_trailing



