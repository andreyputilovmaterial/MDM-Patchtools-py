
from . import handler_base
from . import processor_simple




class FileLoader(handler_base.FileLoader):
    def __init__(self,filecontents):
        super().__init__(filecontents)
        self.register_processor(processor_simple.PatchInsert)
        self.register_processor(processor_simple.PatchReplace)

