
if __name__ == '__main__':
    # run as a program
    import handler_base
    import processor_simple_insert
    import processor_onnextcase
    import processor_metadata
    import processor_section_other_insert
elif '.' in __name__:
    # package
    from . import handler_base
    from . import processor_simple_insert
    from . import processor_onnextcase
    from . import processor_metadata
    from . import processor_section_other_insert
else:
    # included with no parent package
    import handler_base
    import processor_simple_insert
    import processor_onnextcase
    import processor_metadata
    import processor_section_other_insert




class FileLoader(handler_base.FileLoader):
    def __init__(self,filecontents):
        super().__init__(filecontents)
        self.register_processor(processor_simple_insert.PatchInsert)
        self.register_processor(processor_metadata.PatchSectionMetadataInsert)
        self.register_processor(processor_onnextcase.PatchSectionOnNextCaseInsert)
        self.register_processor(processor_section_other_insert.PatchSectionOtherInsert)

