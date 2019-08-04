
init 510 python:

    class LabelLocationCharacterEvent(BaseEvent):
        """
        Subclass to add extra methods
        """
        def get_locations_rest(self, label_str=None):
            """
            Get location(s) from label name and make tests
            church_ari_mus_convo => ['church'], 'ari_mus_convo'
            """
            if not label_str:

                label_str = self.label

            poss_locations = sorted(['anywhere_'] + [
                                     "{}_".format(k.label)
                                     for k in self.handler.location],
                                    key=len, reverse=True)

            locations = []

            for loc in poss_locations:

                if loc in label_str:

                    locations.append(loc[:-1])

                    label_str = label_str.replace(loc, '_')

            return locations, label_str.strip('_')


        def make_location_tests(self, label_str=None):
            """
            Get location(s) from label name and make tests
            church_ari_mus_convo => ['church'], 'ari_mus_convo'
            """
            locations, rest = self.get_locations_rest(label_str)

            if locations:

                self.tests.append(LocationTest(self, args=locations))

            return label_str.strip('_')


        def get_chars_rest(self, label_str=None):
            """
            Get primary characters from label name and make tests
            church_a_mm_convo => ['a','mm'], 'convo'
            """
            if not label_str:

                label_str = self.label

            poss_chars = set( ['anyone_'] + [
                "{}_".format(k) 
                for k in character.__dict__
                if isinstance(getattr(character, k), ADVCharacter)
                and getattr(getattr(character, k), "image_tag", None)])

            # print("Poss Chars: {} : {}".format(poss_chars, 0))

            chars = []

            for char in poss_chars:

                if char in label_str:

                    chars.append(char[:-1])

                    label_str = label_str.replace(char, '_')

            return chars, label_str


        def make_character_tests(self, label_str=None):
            """
            Get location(s) from label name and make tests
            church_ari_mus_convo => ['church'], 'ari_mus_convo'
            """
            chars, rest = self.get_chars_rest(label_str)

            if chars:

                self.tests.append(CharacterTest(self, args=chars))

            return label_str.strip('_')




    class LocationEvent(BaseEvent):


        def __init__(self, handler=None, *tests, **kwargs):

            super(LocationEvent, self).__init__(handler, *tests, **kwargs)

            self.duration = self.handler.get_timedelta("30 days")
            # so as not to clutter the _visits list

            # xpos range : ypos
            self.sprite_positions = {
                (0,1280) : 700
            }

            self.random_item_positions = []


        def get_background(self):

            for test in [ k for k in self.tests if k.ref_name == "option" ]:

                if test.valid:

                    return test.args[0]

            return self.label


        def get_layers(self):

            layers = []

            for test in [ k for k in self.tests if k.ref_name == "layer" ]:

                if test.valid:

                    layers.append(((test.xpos, test.ypos), test.image))

            return layers


        def __repr_extra__(self):

            return " at {}:\n{}".format(
                self.label,
                "\n".join([str(t) for t in self.tests]) )


    class NubEvent(BaseEvent):
        """
        Used so non event labels can store their _visits
        """

        duration = "6 hours"


    class NavigationEvent(LabelLocationCharacterEvent):

        def __init__(self, handler=None, *tests, **kwargs):

            super(NavigationEvent, self).__init__(handler, *tests, **kwargs)

            if not 'on_map' in self.__dict__:

                self.on_map = ["town"]

            loc, _ = self.get_locations_rest(self.label)

            if not loc:

                raise ValueError, "NavigationEvent could not determine " \
                                  "location from label {}".format(self.label)

            self.location = loc[0]


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
                "\n".join([str(t) for t in self.get_paths(False)]) )


        @property
        def valid(self):

            return True
                #    all( 
                # [t.valid for t in self.tests if t.ref_name == "path"] ) 


    class DialogueEvent(LabelLocationCharacterEvent):

        def __init__(self, handler=None, *tests, **kwargs):

            super(DialogueEvent, self).__init__(handler, *tests, **kwargs)

            if not 'auto' in self.__dict__:

                self.auto = True

            rest = self.make_location_tests(self.label)

            rest = self.make_character_tests(rest)

            repeat = [k for k in self.tests if k.ref_name == "repeat"]

            if not repeat:

                self.tests.append(RepeatTest(self, args=[0]))


        def __repr_extra__(self):

            return "\n{}".format(
                "\n".join([str(t) for t in self.tests]) )


        @property
        def valid(self):

            return all( [ t.valid for t in self.tests ] )


    class ItemEvent(LabelLocationCharacterEvent):

        def __init__(self, handler=None, *tests, **kwargs):

            super(ItemEvent, self).__init__(handler, *tests, **kwargs)

            for k,v in {'xpos':100, 'ypos':200, 'image':None}.items():

                if not k in self.__dict__:

                    setattr(self, k, v)

            rest = self.make_location_tests(self.label)

            if not self.image:

                self.image = rest

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
                clicked=Call(self.label),
                anchor=(0.5,0.5),
                pos=(self.xpos, self.ypos))


        def __repr_extra__(self):

            return "{} ({}):\n{}".format(
                self.image,
                (self.xpos, self.ypos),
                "\n".join([str(t) for t in self.tests]) )


        @property
        def valid(self):

            return all( [ t.valid for t in self.tests ] ) 

