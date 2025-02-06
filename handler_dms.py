
if __name__ == '__main__':
    # run as a program
    import handler_base
    import processor_simple
    import processor_onnextcase
    import processor_metadata
    import processor_section_other
elif '.' in __name__:
    # package
    from . import handler_base
    from . import processor_simple
    from . import processor_onnextcase
    from . import processor_metadata
    from . import processor_section_other
else:
    # included with no parent package
    import handler_base
    import processor_simple
    import processor_onnextcase
    import processor_metadata
    import processor_section_other




class FileLoader(handler_base.FileLoader):
    def __init__(self,filecontents):
        super().__init__(filecontents)
        self.register_processor(processor_simple.PatchInsert)
        self.register_processor(processor_simple.PatchReplace)
        self.register_processor(processor_metadata.PatchSectionMetadataInsert)
        self.register_processor(processor_onnextcase.PatchSectionOnNextCaseInsert)
        self.register_processor(processor_section_other.PatchSectionOtherInsert)
        self.register_processor(processor_section_other.PatchSectionOtherReplace)
        self.register_processor(processor_section_other.PatchSectionInputDatasourceInsert)
        self.register_processor(processor_section_other.PatchSectionInputDatasourceReplace)
        self.register_processor(processor_section_other.PatchSectionOutputDatasourceInsert)
        self.register_processor(processor_section_other.PatchSectionOutputDatasourceReplace)

