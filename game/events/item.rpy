# Item labels
# Used to define Item locations within the game

# Important Note:
# Label names should start with a prefix relevant to the location

# Clicking on an Item in game will Call the label itself


            ###############################################
            #                                             #
            #               Town Junctions                #
            #                                             #
            ###############################################



            ###############################################
            #                                             #
            #                 The Bridge                  #
            #                                             #
            ###############################################



            ###############################################
            #                                             #
            #                 The Church                  #
            #                                             #
            ###############################################



            ###############################################
            #                                             #
            #                  The Farm                   #
            #                                             #
            ###############################################



            ###############################################
            #                                             #
            #                 The Forest                  #
            #                                             #
            ###############################################



            ###############################################
            #                                             #
            #               The HiFi Shop                 #
            #                                             #
            ###############################################



            ###############################################
            #                                             #
            #                 The Motel                   #
            #                                             #
            ###############################################



            ###############################################
            #                                             #
            #             The Petrol Station              #
            #                                             #
            ############################################### 



            ###############################################
            #                                             #
            #                The ScrapYard                #
            #                                             #
            ###############################################



            ###############################################
            #                                             #
            #                 The Theater                 #
            #                                             #
            ############################################### 

# label theater_backstage_curtainpin:
#     event register item:
#         (250, 100)
#         unseen "theater_backstage_curtainpin_remove"

#     if current.character == 'a':

#         call theater_backstage_curtainpin_remove

#     else:

#         getattr(character, current.character) "A small pin... just out of reach"

#     return


# label theater_backstage_curtainpin_remove:

#     a "A small pin... useful for adding to eyeballs"

#     a "I will be taking that"

#     "Actually she doesn't... "

#     # Set this label as visited
#     $ eh.visit()

#     return

label theater_storage_key_1:
    event register item:
        "key_theater_stage"
        (250, 100)
        unseen "theater_storage_key_1"

    a happy "The key for the stage door... minesies"

    $ a.alter_item('theater_stage_key')

    $ eh.visit()

    return

label theater_storage_key_2:
    event register item:
        "key_theater_backstage"
        (450, 100)
        unseen "theater_storage_key_2"

    a happy "The key for the backstage door... in the bag with you"

    $ a.alter_item('theater_backstage_key')

    $ eh.visit()

    return


            ###############################################
            #                                             #
            #        The Villa of Hilda Wittberg          #
            #                                             #
            ###############################################



