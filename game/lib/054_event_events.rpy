
init python:

    class LocationEvent(BaseEvent):

        on_map = "town"

        translate_title = _("No Title")
        translate_description = _("No description")

        def __init__(self, handler=None, *tests, **kwargs):

            super(LocationEvent, self).__init__(handler, *tests, **kwargs)

            self.name = self.label[:-9]


        def get_paths(self, valid=True):

            paths = []

            for test in [ k for k in self.tests if k.ref_name == "path" ]:

                if not valid or test.valid:

                    paths.append( test )

            return paths


        def __repr_extra__(self):

            return "({}: {}) with Paths:\n{}".format(
                self.title,
                self.description,
                "\n".join([str(t) for t in self.tests]) )


        @property
        def valid(self):

            return all( [ t.valid for t in self.tests ] ) 

