
init python:

    def location_callback(label=None, context=False):

        global current

        eh.visit(label)

        loc = eh.events.get(label, None)

        if isinstance(loc, LocationEvent):

            current.location = label

            renpy.call('enter_location')

    config.label_callback = location_callback


    def show_char_sprite( char=('a', (100, 100)) ):
        """
        Show the character sprite at the position stated
        Moving to said position if needed
        """

        global current

        tag = getattr(getattr(character, char[0]), "image_tag")

        if not tag:

            raise AttributeError, "No image found for character {}".format(
                char[0])

        start_pos = char[1]

        last_pos = current.sprites.get(tag, None)

        if last_pos and last_pos[0] == current.location:

            start_pos = last_pos[1]

        renpy.show(
                tag,
                at_list=[ move_char_to( tag, start_pos, char[1] ) ] )


    def get_warped_proportion(current_time, max_time, warper='linear'):
        # Utility to return a proportion from the parameters
        # For bound warpers, this will be between 0.0 and 1.0 
        return renpy.atl.warpers[warper.lower()]( current_time / max_time ) 


    def move_sprite_to(tag, start_pos, end_pos, trans, st, at):

        global current

        current_pos = start_pos

        if start_pos != end_pos:

            ratio = get_warped_proportion(st, 1.0, 'ease_cubic')

            ratio = min(1.0, max(0.0, ratio))

            current_pos = (
                start_pos[0] + int(ratio * float(end_pos[0] - start_pos[0])),
                start_pos[1] + int(ratio * float(end_pos[1] - start_pos[1])))

        current.sprites[tag] = [current.location, current_pos]

        # print("{}:{}:{}:{}:{}:{}".format(
        #     tag, start_pos, end_pos, current_pos, st, at))

        trans.pos = current_pos

        if current_pos == end_pos:

            return None

        return 0.0




transform move_char_to(tag, start_pos, end_pos):
    anchor (0.5, 1.0)
    function renpy.curry(move_sprite_to)(tag, start_pos, end_pos)

# The label we Call whenever we enter a new LocationEvent location

label enter_location:

    window hide

    python: 

        current.places[current.character] = current.location

        loc_events = [k for k in eh.location 
                      if k.label == current.location]

        nav_events = [k for k in eh.navigation 
                      if k.location == current.location]

        if len(loc_events) != 1 or len(nav_events) != 1:

            raise ValueError, "Found {} LocationEvent and {} " \
                              "NavigationEvent for {}. Need just 1 of " \
                              "each".format(len(loc_events), 
                                            len(nav_events),
                                            current.location)

        arrows = nav_events[0].get_arrows()

        items = loc_events[0].get_items()

        chars = loc_events[0].get_chars(arrows)

        # char_positions = []

        auto_dialogues = [k for k in eh.dialogue if k.auto]

    scene bg 

    # This ensures the moment spent in the label is part of rollback 
    # and history. 

    # TODO: Try to clean duplicates from rollback too

    $ silent_stan.add_history(
        "adv",
        ">>>",
        " ".join([k.capitalize() for k in current.location.split('_')]), 
        multiple=None)

    # Navigation Buttons

    show screen navigation_buttons([k.get_button() for k in arrows])

    # Any Items lying around?

    show screen item_buttons([k.get_button() for k in items])

    # Visible characters

    while chars:

        $ show_char_sprite( chars.pop() )

    if auto_dialogues:

        # grab the first, then refresh this location in case other 
        # dialogues or stuff appeared

        call expression auto_dialogues.pop(0).label

    else:

        silent_stan ""

    jump expression current.location

    return


screen navigation_buttons(arrows=[]):

    for arrow in arrows:

        add arrow


screen item_buttons(items=[]):

    for item in items:

        add item


init python:

    class SilentStan(ADVCharacter):

        def add_history(self, kind, who, what, multiple=None, **kwargs):
            """
            Only add SilentStan's words to history if the last one wasn't
            the same
            """
            if not hasattr(self, "_last_history_what"):

                self._last_history_what = "_"

            if self._last_history_what == what or what == "":

                return 

            self._last_history_what = what

            super(SilentStan, self).add_history(
                kind, who, what, multiple=multiple, **kwargs)

define silent_stan = SilentStan(
    ">>>", 
    screen="invisible_say")

screen invisible_say(who, what):
    text what id "what" pos (-1000,-1000)
    

init 1 python:

    #
    # This could be extended to provide tinting or compositing etc
    #

    class DynamicBackground(renpy.display.layout.DynamicDisplayable):
        """
        A dynamic background that knows what to show
        """

        def __init__(self, *args, **kwargs):

            self.monitor_vars = [
                "current.location"
            ]

            self.monitor_values = []

            self.cache = None

            kwargs.update( {
                '_predict_function' : self.predict_images } )

            super(DynamicBackground, self).__init__(self.get_background, 
                                                    *args, 
                                                    **kwargs )

        def get_monitored_values(self):
            return [ globals().get(k) for k in self.monitor_vars ]

        def get_background(self, st, at, *args, **kwargs):
            """
            Return background image to use for this time
            """
            current_values = self.get_monitored_values()

            if True:#current_values != self.monitor_values:

                self.monitor_values = current_values

                used_bg = "images/bg/missing_background.png"

                poss_bg = "images/bg/{}.png".format(current.location)

                bg = [k for k in eh.location
                      if k.label == current.location]

                if len(bg) > 1:

                    raise ValueError, "Multiple location labels found for" \
                                      "{}".format(current.location)

                layers = []

                if bg:

                    poss_bg = "images/bg/{}.png".format(
                        bg[0].get_background())

                    layers = bg[0].get_layers()

                if renpy.loadable(poss_bg):

                    used_bg = poss_bg 

                if layers:
                    # A Composite
                    self.cache = Composite(
                        (config.screen_width, config.screen_height),
                        (0,0), used_bg,
                        *[j for k in layers for j in k])

                else:

                    self.cache = used_bg

            return self.cache, 0.1


        def predict_images(self):

            return [ self.cache ]


image bg = DynamicBackground()