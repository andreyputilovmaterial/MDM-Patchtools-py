
if __name__ == '__main__':
    # run as a program
    import handler_base
    import processor_simple_insert
elif '.' in __name__:
    # package
    from . import handler_base
    from . import processor_simple_insert
else:
    # included with no parent package
    import handler_base
    import processor_simple_insert




class FileLoader(handler_base.FileLoader):
    def __init__(self,filecontents):
        super().__init__(filecontents)
        self.register_processor(processor_simple_insert.PatchInsert)

