# https://www.freepik.es/vector-gratis/conjunto-burbujas-texto-comic_1117406.htm


default retained_dialogues = []

init python:

    retained_styles = renpy.screenlang.text_property_names \
                    + renpy.screenlang.position_property_names


    def hide_dialogue( current_dialogue=None, screen="cartoon_dialogue" ):
        """
        Decrease all `retain` values by one and rebuild global
        shown_dialogues only from those set to still be shown

        Then add the current dialogue if it has been set to retain
        """
        global retained_dialogues

        next_retained_dialogues = []

        for k in retained_dialogues:

            k[1] -= 1

            if k[1] > 0:

                next_retained_dialogues.append( k )

        retained_dialogues = next_retained_dialogues

        if current_dialogue and not current_dialogue[0][0].endswith('.rpym'):

            if current_dialogue[1] > 0:

                # retain this one, so add it to the global

                # first mirror the style applied to the text and add it
                # to the kwargs

                widget = renpy.get_widget(screen, 'what')
                if widget:
                    widget_style = {
                        k : getattr(widget.style, k)
                        for k in dir(widget.style)
                        if k in retained_styles
                    }
                    current_dialogue[-1]['what_style'] = widget_style

                retained_dialogues.append( list(current_dialogue) )


style cartoon_speech_ese_frame:

    # Tail: right side lower

    anchor (1.0, 1.0)
    xoffset -40
    yoffset -20

    # our background picture
    background Frame(
        # the image
        Transform("images/ui/bubble.left.lower.png", xzoom=-1),
        # frame borders: the values set left, top, right, base cut sizes
        left = Borders(16, 32, 32, 32)
        )

    # though the frame will adjust to the content, we add these to 
    # make sure the image expands properly to contain the text nicely
    padding (16, 14, 32, 14)


style cartoon_speech_wsw_frame:

    # Tail: left side lower

    anchor (0.0, 1.0)
    xoffset 30
    yoffset -20

    # our background picture
    background Frame(
        # the image
        "images/ui/bubble.left.lower.png", 
        # frame borders: the values set left, top, right, base cut sizes
        left = Borders(32, 32, 16, 32)
        )

    # though the frame will adjust to the content, we add these to 
    # make sure the image expands properly to contain the text nicely
    padding (32, 14, 16, 14)


style cartoon_speech_ssw_frame:

    # Tail: base side left

    anchor (0.0, 1.0)
    xoffset 30
    yoffset -30

    # our background picture
    background Frame(
        # the image
        "images/ui/bubble.base.left.png", 
        # frame borders: the values set left, top, right, base cut sizes
        left = Borders(32, 34, 16, 51)
        )

    # though the frame will adjust to the content, we add these to 
    # make sure the image expands properly to contain the text nicely
    padding (16, 14, 16, 30)


style cartoon_speech_sse_frame:

    # Tail: base side right

    anchor (1.0, 1.0)
    xoffset -30
    yoffset -30

    # our background picture
    background Frame(
        # the image
        Transform("images/ui/bubble.base.left.png", xzoom=-1),
        # frame borders: the values set left, top, right, base cut sizes
        left = Borders(16, 34, 32, 51)
        )

    # though the frame will adjust to the content, we add these to 
    # make sure the image expands properly to contain the text nicely
    padding (16, 14, 16, 30)


style cartoon_speech_text:
    xsize None # needed - otherwise it uses a gui setting
    align (0,0) # also likely needed

    # just standard font specific stuff
    color "#000"
    font "gui/fonts/AsapCondensed-SemiBold.ttf"
    # kerning -1.0
    size 28


screen cartoon_dialogue(who, what, **kwargs):

    # This deactivates the game buttons until dialogue is finished
    button:

        action Function( renpy.end_interaction, 1 )

    $ current_dialogue = (
        renpy.get_filename_line(),
        kwargs.pop('retain', 0),
        who,
        what,
        kwargs )

    # First the older (retained) dialogues
    for idx, old_dialogue in enumerate(retained_dialogues):

        $ old_who, old_what, old_kwargs = old_dialogue[2:]

        $ subat = old_kwargs.get('at', None)

        fixed at subat:

            # set the pos as show_pos if passed else this default
            pos old_kwargs.get( "pos", (250,250) )

            use cartoon_dialogue_component(old_who, **old_kwargs):

                add Text(old_what, **old_kwargs['what_style'])

    # Now the current dialogue

    python:

        kwargs['substyle'] = kwargs.get('substyle', 'speech')

        subat = kwargs.get('at', None)

        # Calculate the pos
        if not kwargs.get( "pos", None ):

            subtag = renpy.get_say_image_tag()

            if subtag:

                subtag_bounds = renpy.get_image_bounds(subtag)

                midpos = (
                    int(subtag_bounds[0] + (subtag_bounds[2]/2)),
                    int(subtag_bounds[1] + (subtag_bounds[3]/2)) )

                current.sprites[subtag] = [
                    current.location, 
                    (midpos[0], int(subtag_bounds[1] + subtag_bounds[3]))]

                leftside = midpos[0] < 641

                upright = subtag_bounds[2] < subtag_bounds[3]

                kwargs['pos'] = (
                    int(subtag_bounds[0] + (
                            subtag_bounds[2] / (2.0 if upright else 6.0))),
                    int(subtag_bounds[1] + (
                            subtag_bounds[3] / (6.0 if upright else 2.0))))

        kwargs['pos'] = kwargs.get( "pos", (640,360) )

        # Now determine the substyle (frame) to use

        kwargs['substyle'] = kwargs.get('substyle', 'speech')

        if not '_' in kwargs['substyle']:

            kwargs['substyle'] = "cartoon_{}".format(kwargs['substyle'])

            # Now work out the actual style

            if kwargs['pos'][1] > 400:

                ext = "ssw" if kwargs['pos'][0] < 641 else "sse"

            else:

                ext = "wsw" if kwargs['pos'][0] < 641 else "ese"

            kwargs['substyle'] = "{}_{}".format(kwargs['substyle'], ext)

    fixed at subat:

        # set the pos as show_pos if passed else this default
        pos kwargs['pos']

        # # Uncomment to show calculated mouth position
        # add Solid('#B676', xysize=(100, 2), anchor=(0.5,0.5))
        # add Solid('#B676', xysize=(2, 100), anchor=(0.5,0.5))

        use cartoon_dialogue_component(who, **kwargs):
        
            text what id "what"

    on "hide":

        action Function(hide_dialogue, 
                        current_dialogue, 
                        "cartoon_dialogue_component")


screen cartoon_dialogue_component(who, **kwargs):

    style_prefix kwargs['substyle']
    
    fixed:

        xmaximum kwargs.get( "width", 320 )

        frame:

            # this single word tells this screen where to use 
            # the indented widgets/attributes (the text part)
            transclude