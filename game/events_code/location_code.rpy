
init python:

    def location_callback(label=None, context=False):

        global current_location

        loc = eh.events.get(label, None)

        if isinstance(loc, LocationEvent):

            eh.visit(label)

            current_location = label

            renpy.call('enter_location')

    config.label_callback = location_callback



# The label we Call whenever we enter a new location

label enter_location:

    window hide

    python: 

        char_locations[current_character] = current_location

        chars = [k for k in char_locations 
                 if char_locations[k] == current_location]

        # Calculate sprite positions

        # char_positions = []

        # dialogues = eh.dialogue

    scene bg 

    # Navigation Buttons

    show screen navigation_buttons(current_location)

    # Any Items lying around?

    show screen item_buttons(current_location)

    # Visible characters

    while chars:

        $ sprite = chars.pop().image_tag

        if sprite:

            show expression sprite:

                anchor (0.5, 1.0)

                pos (200 + (200*len(chars)), 0.9)



    # Do events and stuff



    # This ensures the moment spent in the label is part of rollback 
    # and history. 

    # TODO: Try to clean duplicates from rollback too

    $ current_location_title = " ".join( 
        [k.capitalize() for k in current_location.split('_')])

    silent_stan "Entered: [current_location_title!q]{nw}"

    silent_stan ""

    jump expression current_location

    return


screen navigation_buttons(location=None):

    for nav_event in [k for k in eh.navigation if k.location == location]:

        for arrow in nav_event.get_buttons():

            add arrow


screen item_buttons(location=None):

    for item_event in [k for k in eh.item if k.location == location]:

        add item_event.get_button()

init python:

    class SilentStan(ADVCharacter):

        def add_history(self, kind, who, what, multiple=None, **kwargs):

            previous = _history_list[-1] if _history_list else None 

            if previous and previous.what == what or what == "":

                return 

            super(SilentStan, self).add_history(
                kind, who, what, multiple=multiple, **kwargs)

define silent_stan = SilentStan(
    "Stalker Stan", 
    screen="invisible_say")

screen invisible_say(who, what):
    text what id "what" pos (-1000,-1000)