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


style cartoon_speech_frame:

    # our background picture
    background Frame(
        # the image
        "images/ui/speech.main.32.png", 
        # frame borders
        # see: https://www.renpy.org/doc/html/displayables.html#Frame
        # the values set left, top, right, base cut sizes
        left = Borders(32, 32, 32, 32)
        )

    # though the frame will adjust to the content, we add these to 
    # make sure the image expands properly to contain the text nicely
    padding (24, 20)


style cartoon_speech_text:
    xsize None # needed - otherwise it uses a gui setting
    align (0,0) # also likely needed

    # just standard font specific stuff
    color "#000"
    #font "gui/fonts/GOHAN___.ttf"
    kerning -1.0
    size 22


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

        $ subscr = old_kwargs.get('subscreen', 'cartoon_speech')

        $ subat = old_kwargs.get('at', None)

        fixed at subat:

            # set the pos as show_pos if passed else this default
            pos old_kwargs.get( "pos", (250,250) )

            use expression subscr pass (old_who, **old_kwargs):

                add Text(old_what, **old_kwargs['what_style'])

    # Now the current dialogue
    $ subscr = kwargs.get('subscreen', 'cartoon_speech')

    $ subat = kwargs.get('at', None)

    fixed at subat:

        # set the pos as show_pos if passed else this default
        pos kwargs.get( "pos", (250,250) )

        use expression subscr pass (who, **kwargs):
        
            text what id "what"

    on "hide":

        action Function(hide_dialogue, current_dialogue)


screen cartoon_speech(who, **kwargs):

    style_prefix kwargs.get('substyle', "cartoon_speech")
    
    fixed:

        xmaximum kwargs.get( "width", 320 )

        frame:
            # this single word tells this screen where to use 
            # the indented widgets/attributes (the text part)
            transclude