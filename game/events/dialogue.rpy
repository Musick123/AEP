# Dialogue Labels
# (will likely be separated into different files per person)

# These generally have:
    # A location (where it happens)
    # Characters present (often more than one)
    # Conditional Tests

# The location and initiator are taken from the label name if not 
# expressly set. All dialogue is automatic if conditions are met unless
# auto is set to False

    # label location_character_otherchar_unique:
    #     event register dialogue:
    #         locations "cat" "dog"
    #         characters "yet_another_char"
    #         repeat 1

    # label character_otherchar_unique:
    #     event register dialogue:
    #         "location_1"
    #         "location_2"
    #         repeat 1




label theater_south_2_a_waking_up:
    event register dialogue:
        locations "cat" "dog"
        repeat 1


    a outdoorsleep "Uh-oooh"

    a angry "Where am I? Ohh, I recall I went for little witches..." 

    a normal "Is the party over? It is all silent... Pfft, let's have a look."
        
    return
