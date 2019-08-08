
init python:

    def location_callback(label=None, context=False):

        global current

        loc = eh.events.get(label, None)

        if isinstance(loc, LocationEvent):

            eh.visit(label)

            current.location = label

            renpy.call('enter_location')

    config.label_callback = location_callback



# The label we Call whenever we enter a new LocationEvent location

label enter_location:

    window hide

    python: 

        current.places[current.character] = current.location

        chars = [k for k,v in current.places.items() 
                 if v == current.location]

        # Calculate sprite positions
        # Characters are loaded in across the x range of the location
        # with player character being first

        positions = []


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

    show screen navigation_buttons(current.location)

    # Any Items lying around?

    show screen item_buttons(current.location)

    # Visible characters

    # show ari

    while chars:

        $ sprite = getattr(character, chars.pop()).image_tag

        if sprite:

            $ renpy.show(
                sprite,
                at_list=[Transform(
                    anchor=(0.5, 1.0),
                    pos=(200 + (200*len(chars)), 0.9))])

    if auto_dialogues:

        # grab the first, then refresh this location in case other 
        # dialogues or stuff appeared

        $ auto_dialogue_label = auto_dialogues.pop(0).label

        call expression auto_dialogue_label

        $ eh.visit(auto_dialogue_label)

    else:

        silent_stan ""

    jump expression current.location

    return


screen navigation_buttons(location=None):

    for nav_event in [k for k in eh.navigation if k.location == location]:

        for arrow in nav_event.get_buttons():

            add arrow


screen item_buttons(location=None):

    for item_event in [k for k in eh.item]:

        add item_event.get_button()


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

                    raise ValueError, "Multiple background labels found for" \
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