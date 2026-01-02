
import re




if __name__ == '__main__':
    # run as a program
    import processor_simple
elif '.' in __name__:
    # package
    from . import processor_simple
else:
    # included with no parent package
    import processor_simple








class PatchSectionOtherInsertException(processor_simple.PatchInsertException):
    """Error"""

class PatchSectionOtherInsert(processor_simple.PatchInsert):

    handled_action = 'section/other/insert'

    def __init__(self,txt,regex=None,find_section_name=None):
        # self.txt = txt
        super().__init__(txt)

        self.config = {} # not used, as of now

        self.sections_dict = {}
        if regex is None:
            regex = re.compile(r'((?:^|\n)\s*?event\s*?\(\s*?'+r'(\w+)'+r'\b[^\n]*?\s*?\)\s*?(?:\'[^\n]*?)?\s*?\n)((?:[^\n]*?\n)*?)((?:\s*?\n)*\s*?end\b\s*?\bevent\b)',flags=re.I|re.DOTALL)
        if find_section_name is None:
            find_section_name = lambda txt, section_span: self.sanitize_section_name( txt[ section_span['middle_match'][0] : section_span['middle_match'][1] ] )
        find_regex_results = re.finditer(regex,txt)
        if find_regex_results:
            find_regex_results =  [m for m in find_regex_results] # so that I can refer to multiple items of a generator multiple times
        for index, section_pattern in enumerate(find_regex_results):
            if section_pattern:
                section_span = {
                    'opening_clause': section_pattern.span(1),
                    'middle_match': section_pattern.span(2),
                    'index': index,
                    'body': section_pattern.span(3),
                    'closing_clause': section_pattern.span(4),
                }
                # comment
                # we should ony modify middle part
                # opening clause and closing clause should stay untouched
                section_name = find_section_name(txt,section_span)
                section_txt = self.txt[section_span['opening_clause'][1]:section_span['closing_clause'][0]]
                self.sections_dict[section_name] = {
                    'name': section_name,
                    'section_span': section_span,
                    'section_txt': section_txt,
                    'offset': section_span['opening_clause'][1],
                    'proc': processor_simple.PatchInsert(section_txt),
                }

    def sanitize_section_name(self,section_name):
        if isinstance(section_name,int):
            return section_name
        try:
            m = re.match(r'^\s*?\w+\s*?$',section_name,flags=re.I|re.DOTALL)
            if not m:
                raise Exception(section_name)
        except Exception as e:
            raise Exception('PatchSectionOther: section name must be alphanumeric, no spaces ("{section_name}")'.format(section_name=section_name))
        section_name = re.sub(r'^\s*','',re.sub(r'\s*$','',section_name,flags=re.I|re.DOTALL),flags=re.I|re.DOTALL)
        section_name = section_name.lower()
        return section_name

    def __call__(self, chunk):

        section_name = self.sanitize_section_name(chunk['section'])
        if section_name not in self.sections_dict:
            raise PatchSectionOtherInsertException('section "{s}" not found'.format(s=chunk['section']))
        section = self.sections_dict[section_name]
        proc = section['proc']
        offset = section['offset']

        for p in proc(chunk):
            p['pos'] = p['pos'] + offset
            yield p

class PatchSectionOtherReplace(PatchSectionOtherInsert):

    handled_action = 'section/other/replace'

    def __init__(self,txt,regex=None,find_section_name=None):
        super().__init__(txt,regex,find_section_name)
        for _, section in self.sections_dict.items():
            section['proc'] = processor_simple.PatchReplace(section['section_txt'])



class PatchSectionInputDatasourceInsert(PatchSectionOtherInsert):

    handled_action = 'section/inputdatasource/insert'

    def __init__(self,txt):
        super().__init__(
            txt,
            regex=re.compile(r'((?:^|\n)\s*?InputDatasource\s*?\(?([^\n]*?)\s*?\)?\s*?(?:\'[^\n]*?)?\s*?\n)((?:[^\n]*?\n)*?)((?:\s*?\n)*\s*?end\b\s*?\bInputDatasource\b)',flags=re.I|re.DOTALL),
            find_section_name = lambda txt, section_span: section_span['index'],
        )
    def __call__(self, chunk):
        chunk = {**chunk}
        if not 'section' in chunk:
            chunk['section'] = 0
        yield from super(PatchSectionInputDatasourceInsert,self).__call__(chunk)

class PatchSectionInputDatasourceReplace(PatchSectionOtherReplace):

    handled_action = 'section/inputdatasource/replace'

    def __init__(self,txt):
        super().__init__(
            txt,
            regex=re.compile(r'((?:^|\n)\s*?InputDatasource\s*?\(?([^\n]*?)\s*?\)?\s*?(?:\'[^\n]*?)?\s*?\n)((?:[^\n]*?\n)*?)((?:\s*?\n)*\s*?end\b\s*?\bInputDatasource\b)',flags=re.I|re.DOTALL),
            find_section_name = lambda txt, section_span: section_span['index'],
        )
    def __call__(self, chunk):
        chunk = {**chunk}
        if not 'section' in chunk:
            chunk['section'] = 0
        yield from super(PatchSectionInputDatasourceReplace,self).__call__(chunk)

class PatchSectionOutputDatasourceInsert(PatchSectionOtherInsert):

    handled_action = 'section/outputdatasource/insert'

    def __init__(self,txt):
        super().__init__(
            txt,
            regex=re.compile(r'((?:^|\n)\s*?OutputDatasource\s*?\(?([^\n]*?)\s*?\)?\s*?(?:\'[^\n]*?)?\s*?\n)((?:[^\n]*?\n)*?)((?:\s*?\n)*\s*?end\b\s*?\bOutputDatasource\b)',flags=re.I|re.DOTALL),
            find_section_name = lambda txt, section_span: section_span['index'],
        )
    def __call__(self, chunk):
        chunk = {**chunk}
        chunk['section'] = 0
        yield from super(PatchSectionOutputDatasourceInsert,self).__call__(chunk)

class PatchSectionOutputDatasourceReplace(PatchSectionOtherReplace):

    handled_action = 'section/outputdatasource/replace'

    def __init__(self,txt):
        super().__init__(
            txt,
            regex=re.compile(r'((?:^|\n)\s*?OutputDatasource\s*?\(?([^\n]*?)\s*?\)?\s*?(?:\'[^\n]*?)?\s*?\n)((?:[^\n]*?\n)*?)((?:\s*?\n)*\s*?end\b\s*?\bOutputDatasource\b)',flags=re.I|re.DOTALL),
            find_section_name = lambda txt, section_span: section_span['index'],
        )
    def __call__(self, chunk):
        chunk = {**chunk}
        chunk['section'] = 0
        yield from super(PatchSectionOutputDatasourceReplace,self).__call__(chunk)
