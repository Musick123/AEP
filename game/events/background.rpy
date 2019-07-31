# Conditional background labels
# Just used to define background images and layers to use for any location

# Important Note:
# Label names should start with a prefix relevant to the location
# There is only expected to be one background label per location


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

label church_background:
    event register background:
        alt_bg:
            "church_open" 
            simp "False" # hedge cut?



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

label theater_backstage_background:
    event register background:
        layer:
            "theater_backstage_curtain.png" 
            (0,0)
            unseen "theater_backstage_curtainpin_remove" # cloth not removed


            ###############################################
            #                                             #
            #        The Villa of Hilda Wittberg          #
            #                                             #
            ###############################################



