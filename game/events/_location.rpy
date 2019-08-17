# There is one label at the end of location_code that does most of the work

# Location labels
# These are the labels that we Jump to when we enter a new locations

# Used to define:
    # Available positions for sprites (floor sections)
    # Positions for any random items

# These are NOT expected to contain tests

            ###############################################
            #                                             #
            #               Town Junctions                #
            #                                             #
            ###############################################


label junction_1:
    event register location:
        pass
    return

label junction_2:
    event register location:
        pass
    return

label junction_3:
    event register location:
        pass
    return



            ###############################################
            #                                             #
            #                 The Bridge                  #
            #                                             #
            ###############################################

label bridge:
    event register location:
        pass
    return

            ###############################################
            #                                             #
            #                 The Church                  #
            #                                             #
            ###############################################

label church:
    event register location:
        pass
    return

label church_sanctum:
    event register location:
        pass
    return

label church_gate:
    event register location:
        pass
    return


            ###############################################
            #                                             #
            #                  The Farm                   #
            #                                             #
            ###############################################

label farm:
    event register location:
        pass
    return

label farm_shop:
    event register location:
        pass
    return

label farm_barn:
    event register location:
        pass
    return

label farm_bedroom:
    event register location:
        pass
    return


            ###############################################
            #                                             #
            #                 The Forest                  #
            #                                             #
            ###############################################

label forest:
    event register location:
        pass
    return

            ###############################################
            #                                             #
            #               The HiFi Shop                 #
            #                                             #
            ###############################################

label hifi:
    event register location:
        pass
    return

label hifi_shop:
    event register location:
        pass
    return

label hifi_toilet:
    event register location:
        pass
    return

label hifi_office:
    event register location:
        pass
    return

label hifi_storage:
    event register location:
        pass
    return

label hifi_living:
    event register location:
        pass
    return

label hifi_bath:
    event register location:
        pass
    return

label hifi_bedroom:
    event register location:
        pass
    return

            ###############################################
            #                                             #
            #                 The Motel                   #
            #                                             #
            ###############################################

label motel:
    event register location:
        pass
    return

label motel_lobby:
    event register location:
        pass
    return

label motel_hall_1:
    event register location:
        pass
    return

label motel_hall_2:
    event register location:
        pass
    return

label motel_hall_3:
    event register location:
        pass
    return

label motel_hall_4:
    event register location:
        pass
    return

label motel_hall_5:
    event register location:
        pass
    return

label motel_hall_6:
    event register location:
        pass
    return

label motel_room_1:
    event register location:
        pass
    return

label motel_room_2:
    event register location:
        pass
    return

label motel_room_3:
    event register location:
        pass
    return

label motel_room_4:
    event register location:
        pass
    return

label motel_room_5:
    event register location:
        pass
    return

label motel_room_6:
    event register location:
        pass
    return

label motel_shower:
    event register location:
        pass
    return

# TODO: Motel sub rooms

            ###############################################
            #                                             #
            #             The Petrol Station              #
            #                                             #
            ############################################### 

label petrol:
    event register location:
        pass
    return

label petrol_shop:
    event register location:
        pass
    return

label petrol_toilet:
    event register location:
        pass
    return

label petrol_storage:
    event register location:
        pass
    return

            ###############################################
            #                                             #
            #                The ScrapYard                #
            #                                             #
            ###############################################

label scrap:
    event register location:
        pass
    return

            ###############################################
            #                                             #
            #                 The Theater                 #
            #                                             #
            ###############################################

label theater:
    event register location:
        floor [((415,670), (1180,670))]
    return

label theater_north_1:
    event register location:
        floor [((340,630), (1180,700))]
    return

label theater_north_2:
    event register location:
        floor [((100,690), (1180,770))]
    return

label theater_north_3:
    event register location:
        floor [((100,730), (1180,800))]
    return

label theater_south_1:
    event register location:
        floor [((190,620), (1180,720))]
    return

label theater_south_2:
    event register location:
        floor [((100,660), (510,700)), ((780,710), (1180,730))]
    return

label theater_south_3:
    event register location:
        floor [((100,680), (800,760)), ((801,760), (1180,650))]
    return

label theater_audience:
    event register location:
        floor [((100,650), (300,650))] # Bad - No room for characters
    return

label theater_stage:
    event register location:
        floor [((180,670), (870,670))]
    return

label theater_backstage:
    event register location:
        floor [((100,670), (1180,670))]
        # layer:
        #     "theater_backstage_curtain.png"
        #     (0,0)
        #     unseen "theater_backstage_curtainpin_remove" # cloth not removed
    return

label theater_storage:
    event register location:
        floor [((100,670), (760,670))]
        item:
            "key_theater_stage_idle" 250 100 "theater_storage_key_1"
            unseen "theater_storage_key_1"
        item:
            "key_theater_backstage_idle" 450 100 "theater_storage_key_2"
            unseen "theater_storage_key_2"
    return

            ###############################################
            #                                             #
            #        The Villa of Hilda Wittberg          #
            #                                             #
            ###############################################

label villa:
    event register location:
        pass
    return

label villa_parking:
    event register location:
        pass
    return

label villa_wall:
    event register location:
        pass
    return

label villa_pool:
    event register location:
        pass
    return

# TODO: Find out what Villa looks like as pdf is confusing
#       with saloon and pool being indistinct

# label villa_hall:
#     event register location:
#         path 'villa_wall' 25
#     return

# label villa_saloon:
#     event register location:
#         path 'villa_wall' 25
#     return

# label villa_guest:
#     event register location:
#         path 'villa_wall' 25
#     return

# label villa_bath:
#     event register location:
#         path 'villa_wall' 25
#     return

# label villa_kitchen:
#     event register location:
#         path 'villa_wall' 25
#     return

# label villa_bedroom:
#     event register location:
#         path 'villa_wall' 25
#     return

# label villa_cellar:
#     event register location:
#         path 'villa_wall' 25
#     return


