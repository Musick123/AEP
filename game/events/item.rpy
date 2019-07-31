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

label theater_backstage_curtainpin:
    event register item:
        (250, 100)
        unseen "theater_backstage_curtainpin_remove"

    if current_character == a:

        call theater_backstage_curtainpin_remove

    else:

        current_character "A small pin... just out of reach"

    jump expression current_location


label theater_backstage_curtainpin_remove:

    a "A small pin... useful for adding to eyeballs"

    a "I will be taking that"

    # Set this label as visited
    $ eh.visit()

    jump expression current_location


            ###############################################
            #                                             #
            #        The Villa of Hilda Wittberg          #
            #                                             #
            ###############################################



