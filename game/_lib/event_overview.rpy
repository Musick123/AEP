

style event_overview_text is default:
    size 14

style event_overview_button is default:
    xfill True
    yfill True
    background Frame(
            Text( "\u25A2", 
                  color="#828282", 
                  font="DejaVuSans.ttf", 
                  size=36, 
                  xfill=True,
                ),
            8,8,
            tile=False)
    hover_background Frame(
            Text( "\u25A2", 
                  color="#B2B2B2", 
                  font="DejaVuSans.ttf", 
                  size=36, 
                  xfill=True,
                ),
            8,8,
            tile=False)
    selected_background Frame(
            Text( "\u25A2", 
                  color="#82B282", 
                  font="DejaVuSans.ttf", 
                  size=36, 
                  xfill=True,
                ),
            8,8,
            tile=False)
    selected_hover_background Frame(
            Text( "\u25A2", 
                  color="#A2D2A2", 
                  font="DejaVuSans.ttf", 
                  size=36, 
                  xfill=True,
                ),
            8,8,
            tile=False)
    focus_mask Frame(
            Text( "\u25A0", 
                  color="#828282", 
                  font="DejaVuSans.ttf", 
                  size=36, 
                  xfill=True,
                ),
            8,8,
            tile=False)

style event_overview_button_text is default:
    anchor (0.5,0.5)
    align (0.5,0.5)
    yoffset 2
    size 16


default frame_bg = Frame(
            Text( "\u25A2", 
                  color="#828282", 
                  font="DejaVuSans.ttf", 
                  size=48, 
                  outlines=[
                    (0, "#161616", absolute(2), absolute(2)),
                    (0, "#BCBCBC", absolute(-2), absolute(-2))]), 
            24, 24,
            tile=False)


default persistent.event_overview_persistent_data = {
    'vmax_lines' : 75,
    'vevent_type' : [],
    'vtime_unit' : 'hours'
} 

screen event_overview():

    modal True

    layer "screens"

    style_prefix "event_overview"

    add Solid("#464646") 

    frame:
        margin (5,5)
        padding (10,10)
        background frame_bg

        fixed:
            area (0,0, 1.0, 1.0)

            fixed:
                area (0,0, 0.2, 0.1)

                frame:
                    xfill True
                    yfill True
                    padding (20,25)
                    background frame_bg

                    fixed:
                        text "[eh]" size 21

            fixed:
                area (0,0.08, 0.2, 0.92)

                frame:
                    xfill True
                    yfill True
                    padding (10,15)
                    background frame_bg

                    fixed:
                        area (0.0, 0.0, 1.0, 0.8)

                        use time_buttons

                    fixed:
                        area (0.0, 0.8, 1.0, 0.2)

                        use event_type_buttons#language_buttons

            fixed:
                area (0.2, 0, 0.8, 1.0)

                frame:
                    xfill True
                    yfill True
                    padding (10,15)
                    background frame_bg

                    fixed:
                        area (0.0, 0.0, 1.0, 1.0)

                        use event_info()


screen time_buttons():

    $ pers_dict = persistent.event_overview_persistent_data

    vbox:

        hbox:
            for k in ['mins', 'hours', 'days']:
                textbutton "[k]":
                    xysize (75,42)
                    action SetDict(
                        pers_dict,
                        'vtime_unit',
                        'minutes' if k == 'mins' else k )

        fixed:

            if pers_dict.get('vtime_unit', 'hours') == 'minutes':

                grid 2 7:
                    # spacing 4
                    for k in [1,2,5,10,15,30,45]:
                        textbutton "-[k] mins":
                            xysize (110,42)
                            action Function(eh.time, minutes=k*-1)
                        textbutton "+[k] mins":
                            xysize (110,42)
                            action Function(eh.time, minutes=k)

            elif pers_dict.get('vtime_unit', 'hours') == 'hours':

                grid 2 6:
                    # spacing 4
                    for k in [1,2,3,6,12,24]:
                        textbutton "-[k] hours":
                            xysize (110,42)
                            action Function(eh.time, hours=k*-1)
                        textbutton "+[k] hours":
                            xysize (110,42)
                            action Function(eh.time, hours=k)

            else:

                grid 2 7:
                    # spacing 4
                    for k in [1,2,4,8,16,32,64]:
                        textbutton "-[k] days":
                            xysize (110,42)
                            action Function(eh.time, days=k*-1)
                        textbutton "+[k] days":
                            xysize (110,42)
                            action Function(eh.time, days=k)



screen event_info():

    # \u25CF circle
    # \u2714 tick
    # \u2718 cross
    # \u2047 double question mark
    # \u2370 ? in a box

    python:

        eopd = persistent.event_overview_persistent_data

        events = globals()[ eh_init_values['ref'] ].get_type_events(
            eopd.get( 'vevent_type', [] ), valid=False ) 

        eh_max_lines = eopd.get( 'vmax_lines', 75)

        true_string = "{size=+4}{font=DejaVuSans.ttf}\u2714{/font}{/size}"

        true_icon = ( "{color=#4E4}" + true_string + "{/color}" )

        false_icon = (
            "{size=+4}{font=DejaVuSans.ttf}" \
            "{color=#F33}\u2718{/color}" \
            "{/font}{/size}" )

    vbox:

        spacing 2

        if not len(events):

            text "No Data Found"

        else:

            fixed:
                area (0,0, 1.0, 34)

                frame:
                    background Solid("#555A")
                    padding (5, 10)

                    fixed:
                        area (0,0, 0.025, 1.0)
                        text true_string yoffset -2

                    fixed:
                        area (0.025,0, 0.2, 1.0)
                        text "Label Name"

                    fixed:
                        area (0.225,0, 0.775, 1.0)
                        text "Event Repr"

        viewport:
            draggable True
            mousewheel True
            scrollbars None

            vbox:

                spacing 2

                for idx, event in enumerate(events[:eh_max_lines]):

                    fixed:
                        area (0,0, 1.0, 26)

                        frame:

                            background Solid("#AAAA" if idx % 2 else "#AAA8")

                            fixed:
                                area (0,0, 0.025, 1.0)
                                textbutton (true_icon if event.valid 
                                      else false_icon):
                                    focus_mask None
                                    background None
                                    hover_background None
                                    yoffset -2
                                    action Function( 
                                        renpy.show_screen, 
                                        'event_test_info',
                                        event.label )

                            fixed:
                                area (0.025,0, 0.2, 1.0)
                                viewport:
                                    draggable True
                                    scrollbars None

                                    text str(event.label) layout "nobreak"

                            fixed:
                                area (0.225,0, 0.775, 1.0)
                                viewport:
                                    draggable True
                                    scrollbars None

                                    text "[event!q]" layout "nobreak"


screen event_test_info(label=None):

    style_prefix "event_overview"

    python:

        mpos = renpy.get_mouse_pos()

    fixed:

        button:

            style "default"
            action Function( renpy.hide_screen, 'event_test_info' )


        drag:
            drag_name "test_info"
            pos (mpos[0]+5, mpos[1]-25)
            drag_handle (0, 0, 1.0, 78)

            fixed:

                area (0,0, 500, 300)

                button:

                    background None
                    hover_background None

                    action NullAction()

                    fixed:

                        use event_test_results(label)


screen event_test_results(label=None):

    style_prefix "event_overview"

    python:

        event = globals()[ eh_init_values['ref'] ].get_event( label )

        test_reprs = [ repr(t) for t in event.tests ]

        def iconify_str(s=""):

            r = str(s).replace("{", "{{")
            r = r.replace("}", "}}")
            r = r.replace("[", "[[")
            r = r.replace("]", "]]")
            r = r.replace("%", "%%")
            r = r.replace(
                ":pass:", ( 
                    "{size=+4}{font=DejaVuSans.ttf}" \
                    "{color=#4E4}\u2714{/color}" \
                    "{/font}{/size}" ) )
            r = r.replace(
                ":fail:", (
                    "{size=+4}{font=DejaVuSans.ttf}" \
                    "{color=#F33}\u2718{/color}" \
                    "{/font}{/size}" ) ) 
            return r

    add Solid("#464646", pos=(10,16), xysize=(480, 274)) 

    frame:
        xfill True
        yfill True
        padding (10,10)
        background frame_bg

        fixed:
            area (0,0, 1.0, 1.0)

            fixed:
                area (0,0, 1.0, 58)

                frame:
                    xfill True
                    yfill True
                    padding (20,22)
                    background frame_bg

                    fixed:
                        text "Test Results for [label]":
                            size 18
                            xanchor 0.5
                            xalign 0.5

            fixed:
                area (5,58, 470, 216)

                viewport:

                    draggable True
                    mousewheel True
                    scrollbars None

                    vbox:

                        for idx, test_repr in enumerate( test_reprs ):

                            # fixed:

                            frame:
                                xminimum 468

                                background Solid( "#AAAA" if idx % 2 
                                                  else "#AAA8")

                                text iconify_str( test_repr ):

                                    layout "nobreak"


screen language_buttons():

    fixed:
        area (0,0, 1.0, 1.0)

        vbox:
            text "Language: " pos (4,7)

            textbutton "Default":
                xysize (150, 42)
                selected (_preferences.language == None)
                action [ 
                    Function(renpy.change_language, None),
                    Function(renpy.restart_interaction),
                    Hide("say") ]

            for language in sorted( renpy.known_languages() ):

                textbutton "{}".format(language.capitalize()):
                    xysize (150, 42)
                    selected (
                        _preferences.language == language )
                    action [ 
                        Function(renpy.change_language, language),
                        Function(renpy.restart_interaction),
                        Hide("say") ]


screen event_type_buttons():

    python:

        eopd = persistent.event_overview_persistent_data

        event_types = sorted( [
            k for k in 
            globals()[ eh_init_values['ref'] ].event_factory.event_types ] )

        if not eopd['vevent_type']:

            eopd['vevent_type'] = event_types

    fixed:
        area (0,0, 1.0, 1.0)

        vbox:
            text "Event Types:" pos (4,7)

            for event_type in event_types:

                textbutton "{}".format(
                        " ".join( [ k.capitalize() 
                                    for k in event_type.split('_') ] ) ):
                    xysize (150, 42)
                    selected event_type in eopd['vevent_type']
                    action [ If(
                            event_type in eopd['vevent_type'],
                            RemoveFromSet(eopd['vevent_type'], event_type),
                            AddToSet(eopd['vevent_type'], event_type) ),
                        Function(renpy.restart_interaction) ]


init python:

    if config.developer == True:

        config.underlay.append(
            renpy.Keymap( 
                alt_K_a = lambda: renpy.run( 
                                    ToggleScreen("event_overview") ) 
            )
        )