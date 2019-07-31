
init python:

    class LabelLocationEvent(BaseEvent):
        """
        Subclass to add extra methods
        """
        def get_location_rest(self, label_str=None):

            if not label_str:

                label_str = self.label

            labels = sorted([k.label for k in self.handler.location
                             if label_str.startswith(k.label)],
                            key=len)

            if not labels:

                return None, self.label 

            if len(labels) > 1:

                if len(labels[-1]) == len(labels[-2]):

                    raise ValueError, "Could not find unique location " \
                                      "from '{}'".format(label_str)

            return labels[-1], label_str[ len(labels[-1]) : ].strip('_')


        def get_characters_rest(self, label_str=None):

            if not label_str:

                label_str = self.label

            poss_chars = ['a','r','mm']

            test_parts = label_str.split('_')

            if not test_parts:

                return [], ""

            chars, rest = [], []

            for tpc,tp in enumerate(test_parts):

                if tp in poss_chars:

                    chars.append(tp)

                    continue 

                else:

                    rest.extend(test_parts[tpc:])

                    break

            return chars, "_".join(rest)


    class BackgroundEvent(LabelLocationEvent):

        location = None

        def __init__(self, handler=None, *tests, **kwargs):

            super(BackgroundEvent, self).__init__(handler, *tests, **kwargs)

            loc, _ = self.get_location_rest(self.label)

            if not loc:

                raise ValueError, "Background could not determine " \
                                  "location from label {}".format(self.label)

            self.location = loc

        def get_background(self):

            paths = []

            for test in [ k for k in self.tests if k.ref_name == "option" ]:

                if test.valid:

                    return test.args[0]

            return self.location

        def get_layers(self):

            layers = []

            for test in [ k for k in self.tests if k.ref_name == "layer" ]:

                if test.valid:

                    layers.append(((test.xpos, test.ypos), test.image))

            return layers

        def __repr_extra__(self):

            return " at {}:\n{}".format(
                self.location,
                "\n".join([str(t) for t in self.tests]) )


    class NubEvent(BaseEvent):
        """
        Used so non event labels can store their _visits
        """

        duration = "6 hours"


    class LocationEvent(BaseEvent):

        # xpos range : ypos
        sprite_positions = {
            (0,1280) : 700
        }

        random_item_positions = []

        duration = "10 years" # so as not to clutter the _visits list


    class NavigationEvent(LabelLocationEvent):

        on_map = ["town"]

        location = None

        def __init__(self, handler=None, *tests, **kwargs):

            super(NavigationEvent, self).__init__(handler, *tests, **kwargs)

            loc, _ = self.get_location_rest(self.label)

            if not loc:

                raise ValueError, "NavigationEvent could not determine " \
                                  "location from label {}".format(self.label)

            self.location = loc


        def get_paths(self, valid=True):

            paths = []

            for test in [ k for k in self.tests if k.ref_name == "path" ]:

                if not valid or test.valid:

                    paths.append( test )

            return paths


        def get_buttons(self):

            return [k.get_button() for k in self.tests 
                    if k.ref_name == "arrow" 
                    and k.valid]


        def __repr_extra__(self):

            return "{} with Paths:\n{}".format(
                self.location,
                "\n".join([str(t) for t in self.tests]) )


        @property
        def valid(self):

            return True
                #    all( 
                # [t.valid for t in self.tests if t.ref_name == "path"] ) 


    class DialogueEvent(LabelLocationEvent):

        locations = [] 
        characters = []
        auto = True

        def __init__(self, handler=None, *tests, **kwargs):

            super(DialogueEvent, self).__init__(handler, *tests, **kwargs)

            if self.args:

                self.locations.extend(self.args)

            label_info = self.label[:]

            loc, _ = self.get_location_rest(label_info)

            if loc:

                self.locations.append(loc)

            chars, _ = self.get_characters_rest(label_info)

            if chars:

                self.characters = chars + self.characters


        def __repr_extra__(self):

            return " at {} with {}:\n{}".format(
                self.locations,
                self.characters,
                "\n".join([str(t) for t in self.tests]) )


        @property
        def valid(self):

            if (self.locations 
                and "anywhere" not in self.locations
                and current_location not in self.locations):

                return False

            if (self.characters
                and "anyone" not in self.characters
                and not all([
                    character_locations[getattr(character,k)] 
                        == current_location 
                    for k in self.characters])):

                return False

            return all( [ t.valid for t in self.tests ] )


    class ItemEvent(LabelLocationEvent):

        location = None
        xpos = 100
        ypos = 200
        image = None

        def __init__(self, handler=None, *tests, **kwargs):

            super(ItemEvent, self).__init__(handler, *tests, **kwargs)

            if not self.location:

                loc, _ = self.get_location_rest(self.label)

                if not loc:

                    raise ValueError, "Item could not determine location " \
                                      "from label {}".format(self.label)

                self.location = loc

            if not self.image:

                self.image = self.label[:]

            pos_values = []

            for arg in self.args:

                if isinstance(arg, (int, float)):

                    pos_values.append(arg)

                elif isinstance(arg, renpy.ast.PyExpr):

                    pos_values.extend(list(renpy.python.py_eval(arg)))

                elif isinstance(arg, basestring):

                    self.image = arg

                else:

                    raise AttributeError, "ItemEvent got an invalid " \
                                          "argument {}".format(arg)

            if pos_values:

                if len(pos_values) > 2:

                    raise AttributeError, "ItemEvent received too many " \
                                          "position values"

                self.xpos = pos_values[0]

                if len(pos_values) == 2:

                    self.ypos = pos_values[1]

            if not renpy.loadable(self.image):

                if renpy.loadable("images/items/{}.png".format(self.image)):

                    self.image = "images/items/{}.png".format(self.image)

                else:

                    raise AttributeError, "ItemEvent could not find image " \
                                          "from {}".format(self.image)


        def get_button(self):

            return ImageButton(
                self.image,
                clicked=Jump(self.label),
                anchor=(0.5,0.5),
                pos=(self.xpos, self.ypos))


        def __repr_extra__(self):

            return "{} at {}:\n{}".format(
                self.image,
                self.location,
                "\n".join([str(t) for t in self.tests]) )


        @property
        def valid(self):

            if self.location and current_location != self.location:

                return False

            return all( [ t.valid for t in self.tests ] ) 

