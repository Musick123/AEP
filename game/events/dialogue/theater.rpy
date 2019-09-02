# Dialogue Labels

# These generally have:
    # A location (where it happens)
    # Characters present (sometimes more than one)
    # Conditional Tests

# The location and initiator are taken from the label name if not 
# expressly set. All dialogue is automatic if conditions are met unless
# auto is set to False


label theater_south_2_a_waking_up:
    event register dialogue:
        pass

    $ a.state = 'outdoorsleep'

    show ari: # On this one we put her at a set place on screen
        pos (410,700)

    a "Uh-oooh"

    a "Where am I? Ohh, I recall I went for little witches..." 

    $ a.state = None
    
    a angry "Is the party over? It is all silent... Pfft, let's have a look."
        
    return

label theater_a_first_visit:
    event register dialogue:
        pass

    a "Looks like all the cars are gone"
        
    return


label theater_audience_a_first_visit:
    event register dialogue:
        pass

    a "A little robot"
        
    return

# label theater_north_1_a_first_visit:
#     event register dialogue:
#         pass

#     a ""

#     return

# label theater_north_2_a_first_visit:
#     event register dialogue:
#         pass

#     a ""

#     return
