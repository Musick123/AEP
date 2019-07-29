
init python:

    class BackgroundEvent(BaseEvent):

        default = None

        def __init__(self, handler=None, *tests, **kwargs):

            super(BackgroundEvent, self).__init__(handler, *tests, **kwargs)

            self.default = self.label.rpartition('_')[0]


        def get_value(self):

            paths = []

            for test in [ k for k in self.tests if k.ref_name == "option" ]:

                if test.valid:

                    return test.args[0]

            return self.default

    class LocationEvent(BaseEvent):

        # xpos range : ypos
        sprite_positions = {
            (0,1280) : 700
        }

        random_item_positions = []

        duration = "10 years" # so as not to clutter the _visits list


    class NavigationEvent(BaseEvent):

        on_map = ["town"]

        translate_title = _("No Title")
        translate_description = _("No description")

        def __init__(self, handler=None, *tests, **kwargs):

            super(NavigationEvent, self).__init__(handler, *tests, **kwargs)

            self.name = self.label.rpartition('_')[0]


        def get_paths(self, valid=True):

            paths = []

            for test in [ k for k in self.tests if k.ref_name == "path" ]:

                if not valid or test.valid:

                    paths.append( test )

            return paths


        def get_buttons(self):

            return [k.get_button() for k in self.tests 
                    if k.ref_name == "arrow" ]


        def __repr_extra__(self):

            return "({}: {}) with Paths:\n{}".format(
                self.title,
                self.description,
                "\n".join([str(t) for t in self.tests]) )


        @property
        def valid(self):

            return all( [ t.valid for t in self.tests ] ) 

