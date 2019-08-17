
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

            # Positions for sprites in this location
            #
            # Used to say where the floor is (can use multiple sectors)
            # [ ((x0,y0),(x1,y1)) ((x2,y2),(x3,y3)) ]
            self.floor = kwargs.get('floor', None)
            if self.floor:
                self.floor = renpy.python.py_eval(self.floor[0])
            else:
                self.floor = [((150,710), (1130, 710))]
            # We offset characters away from buttons and items too

            # Positions of random items
            self.rand_pos = []


        def get_chars(self, arrows=[]):
            """
            Return ('ref',x,y) tuples for the (0.5,1.0) feet anchor 
            for each char in render order (controlled character last)
            """

            # Determine available xpos ranges (avoiding items)
            items = arrows + self.get_items()
            item_places = [(k.xpos-49, k.xpos+49) for k in items]
            # [ (120,160), (310,350) ]

            vectors = []
            for start, end in self.floor:

                if start[0] > end[0]:

                    start, end = end, start

                points = []

                xpos = start[0]

                while xpos <= end[0]:

                    if not any([xpos in range(*k) for k in item_places]):

                        # Add it to points

                        points.append( (xpos, int(
                                start[1] + (
                                    (float(xpos - start[0]) 
                                     / float(end[0] - start[0])) 
                                    * (end[1] - start[1])))) )

                        # Move to next invalid xpos and add a point

                        next_item = sorted(
                            [k[0] for k in item_places if k[0] > xpos] )

                        if not next_item or next_item[0] > end[0]:

                            xpos = end[0]

                            points.append( end )

                            xpos += 1

                        else:

                            xpos = next_item[0] - 1

                            points.append( (xpos, int(
                                    start[1] + (
                                        (float(xpos - start[0]) 
                                         / float(end[0] - start[0])) 
                                        * (end[1] - start[1])))) )

                            xpos += 1

                    else:

                        # Move to first valid xpos (or past end)

                        next_item = sorted(
                            [k[1] for k in item_places if k[1] > xpos] )

                        if not next_item:

                            xpos = end[0] + 1

                        else:

                            xpos = next_item[0] + 1

                vectors.extend(points)

            vectors = [(vectors[k], vectors[k+1]) 
                       for k in range(0, len(vectors), 2)]

            other_chars = [k for k,v in current.places.items() 
                           if v == current.location 
                           and k != current.character]
            char_places = [ current.character ]

            for idx, other_char in enumerate(other_chars):

                if idx % 2:
                    char_places = [ other_char ] + char_places
                else:
                    char_places = char_places + [ other_char ]


            float_xs = [(1.0/float(len(char_places)*2)) 
                        * ((k*2)+1) for k in range(len(char_places)) ]
            # [1.0 / (len(char_places) + 1) * (k + 1) 
            #             for k in range(len(char_places))]

            chars = [] # [ ('a', (120,710)) ]

            x_vals_in_vectors = sum( [ k[1][0] - k[0][0] for k in vectors ] )

            for idx, char in enumerate(char_places):

                # Calculate the xpos, ypos

                xval = int(x_vals_in_vectors * float_xs[idx])

                for start, end in vectors:

                    vector_width = end[0] - start[0]

                    if xval <= vector_width:

                        # This char is in this vector

                        xpos = start[0] + xval

                        chars.append( (char, (xpos, int(
                                    start[1] + (
                                        (float(xpos - start[0]) 
                                         / float(end[0] - start[0])) 
                                        * (end[1] - start[1]))))) )

                        break

                    else:

                        xval -= end[0] - start[0]

            # print("Floor:{}\nItems:{}\nAllowed:{}\nChars:{}".format(
            #     self.floor,
            #     item_places,
            #     vectors,
            #     chars))

            return chars


        def get_background(self):

            for test in [ k for k in self.tests if k.ref_name == "alt_bg" ]:

                if test.valid:

                    return test.args[0]

            return self.label


        def get_layers(self):

            layers = []

            for test in [ k for k in self.tests if k.ref_name == "layer" ]:

                if test.valid:

                    layers.append(((test.xpos, test.ypos), test.image))

            return layers


        def get_items(self, valid=True):

            items = []

            for test in [ k for k in self.tests if k.ref_name == "item" ]:

                if not valid or test.valid:

                    items.append( test )

            return items


        @property
        def valid(self):
            return True


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


        def get_arrows(self, valid=True):

            arrows = []

            for test in [ k for k in self.tests if k.ref_name == "arrow" ]:

                if not valid or test.valid:

                    arrows.append( test )

            return arrows


        def __repr_extra__(self):

            return "{} with Paths:\n{}".format(
                self.location,
                "\n".join([str(t) for t in self.get_paths(False)]) )


        @property
        def valid(self):
            return True


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


