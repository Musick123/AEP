
python early:

    #
    # Lexer code to handle the 'event' tags

    # Until I find a better way...
    file_line_label_map = {}

    def get_label_for_node(filename, linenumber):
        """ 
        Return label name relevant for the filename and linenumber
        """ 
        if not len(file_line_label_map):
            poss_labels = [ k for k in renpy.get_all_labels() if k[0] != '_' ]
            for k in poss_labels:
                fn = renpy.game.script.namemap[k].filename
                ln = renpy.game.script.namemap[k].linenumber
                if not fn in file_line_label_map:
                    file_line_label_map[ fn ] = []
                file_line_label_map[ fn ].append( ( ln, k ) )
            for fn in file_line_label_map:
                # sort reverse
                file_line_label_map[ fn ].sort( key=lambda r:-r[0] )
        if filename in file_line_label_map:
            for lineno, label in file_line_label_map[ filename ]:
                if lineno < linenumber:
                    return label
        return False


    def get_list_from_node(lexer, node_list=[]):
        """ 
        Compile the node into a list where each element is
        a list of values for the line
        with each block being a nested sub-list
        """
        while lexer.advance():

            # get the values from the line
            line_vals = get_values_from_line( lexer )

            if line_vals:

                if line_vals[-1] == ":":

                    # We are in a block

                    if len(line_vals) < 2:

                        lexer.error("""Parser encountered a : without
                                       a previous keyword""" )

                    if len(line_vals) > 2:

                        lexer.error("""Parser encountered a : with extra
                                       values after the keyword""" )

                    sub_node_list = get_list_from_node(
                        lexer.subblock_lexer(), [] )

                    node_list.append( [ line_vals[-2], sub_node_list ] )

                elif len(line_vals) == 1:

                    # arg or single value

                    node_list.append( line_vals )

                else:

                    # normal line with multiple values (set as [kw, list] )

                    node_list.append( [ line_vals[0], line_vals[1:] ] )

        return node_list


    def get_values_from_line(lexer):
        """ 
        Interpret the line and return args and kwargs
        """
        values = []

        while True:

            value = get_next_value_from_line( lexer )

            if not value:

                break

            else:

                values.append( value )

        return values


    def get_next_value_from_line(lexer):
        """
        Return the next logical value from line 
        and move the lexer position past it 
        """
        lexer.skip_whitespace()

        # End of line
        if lexer.eol():
            return None

        # keyword (used for kwarg = value pairs)
        value = lexer.word()
        if value:
            if value != "_":
                return value
            lexer.pos -= 1

        curpos = lexer.pos
        # float or integer value
        value = lexer.float()
        if value:
            # check it is a real float and not a floated int
            lexer.pos = curpos
            # integer value
            ivalue = lexer.integer()
            if ivalue and float(ivalue) == float(value):
                return int(value)

            lexer.pos = curpos
            value = float(lexer.float())
            return value

        # python string ( anything between '' or "" or `` pairs )
        curpos = lexer.pos
        if lexer.python_string():
            return lexer.text[ curpos+1:lexer.pos-1 ]
        lexer.pos = curpos

        # simple expression ( maybe never used as mostly in strings )
        value = lexer.simple_expression()
        if value:
            return value

        # lists, sets, dicts ( anything between [] or () or {} pairs )
        curpos = lexer.pos
        if lexer.parenthesised_python():
            return lexer.text[ curpos:lexer.pos ]
        lexer.pos = curpos

        # fall through
        return lexer.rest()



    #
    # event time/minute
    #

    # def event_time_parse(lexer):
    #     """ 
    #     Handle parsing of the Ren'py sub-tag 'event time' 
    #     """
    #     location = lexer.get_location()
        
    #     minutes = lexer.integer()
        
    #     if not minutes:
    #         minutes = lexer.string()
        
    #     lexer.expect_eol()
        
    #     return ( minutes, location )

    # def event_time_execute(args):
    #     """ 
    #     Handle execution of the Ren'py sub-tag 'event time' 
    #     """
    #     label = get_label_for_node( *args[1] )

    #     globals()[ eh_init_values['ref'] ].time( args[0], label=label )


    # def event_time_lint(args):
    #     """ 
    #     Handle lint testing of the Ren'py sub-tag 'event time' 
    #     """
    #     pass


    # renpy.register_statement(
    #     "event time",
    #     parse = event_time_parse,
    #     execute = event_time_execute,
    #     lint = event_time_lint,
    # )

    #
    # event register
    #

    def event_register_parse(lexer):
        """ 
        Handle parsing of the Ren'py tag 'event register' 
        """
        vals = [ k for k in get_values_from_line(lexer) if k != ":" ]

        node_lexer = lexer.subblock_lexer()

        event_node_list = get_list_from_node( 
            node_lexer, 
            [ ['type', vals ] ] )
        
        event_node_list.append(lexer.get_location())
        
        return event_node_list


    def event_register_execute(event_node_list):
        """ 
        Handle execution of the Ren'py tag 'event register' 
        """
        label = get_label_for_node( *event_node_list[-1] )

        globals()[ eh_init_values['ref'] ].register_event(
            label, 
            *event_node_list[:-1] )


    def event_register_lint(event_node_list):
        """ 
        Handle lint testing of the Ren'py tag 'event register' 
        """
        pass


    renpy.register_statement(
        "event register",
        parse = event_register_parse,
        execute = event_register_execute,
        lint = event_register_lint,
        # translatable = True,
        block = True,
        init = True,
        init_priority = 550
    )